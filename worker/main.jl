#### Collatz Conjecture testing program
# https://en.wikipedia.org/wiki/Collatz_conjecture

## ./data
# the data file is in the following format:
# worker_id,starting_value,goal,current_value (optional)

# worker_id is the id that has been asigned to this worker.
# it is used when the assigned range has been fully computed
# to report success.

# starting_value is the value from which computations start.
# it is used as a fallback if current_value is not there.

# goal is the number up to which computation will occour.
# when this number is reached we can report success.

# current_value is our current progress in our computations.
# when chunks are computed current_value is incremented to
# reflect the numbers we have scanned. If not present
# starting_value can be used as a fallback.

# below is the mathematical reasoning behind the 4n + 3 search space.
#
# 2n -> n and n < 2n so discard 2n leaving 2n + 1
# split 2n + 1 into 4n + 1, 4n + 3
# 4n + 1 (odd) -> 1.5(4n + 1) + 0.5 = 6n + 2 = 3n + 1 and 3n + 1 < 4n + 1 so discard 4n + 1 leaving 4n + 3
# 4n + 3 can be split but cannot be narrowed further.

# a) if the number enters a loop that excludes 1
# b) if the number grows without bounds and tends to infinity.
# In either of these cases then the test function will block forever (intended behavior)

# If a number ever falls below it's starting value it can be discarded. There are two ways of justifying this.
#
# a) since we are testing numbers starting low and going up, if a number ever drops below it's starting value
# then it must now be at a number we have already tested and found to be "normal" (does not break the conjecture)
#
# b) lets say that we are only searching for the lowest counterexample to the conjecture, then if a counterexample falls
# below it's starting value then we have found another lower counterexample so the first could not have been the lowest.
# this is because if n is a counterexample then EVERY number in it's sequence also must be a counterexample coz common sense.

# terminology:
# chunk: A range of numbers consisting of start and end points that covers every single integer in the range.
# range: A range of numbers that only covers certain values within that range. This is used to split chunks amounst threads or to exclude fallen ranges.

# TODO: Benchmark out-of-loop precomputation of the first two 1.5n+1 steps and passing in both values vs computing in function.

# TODO: Try putting all the below into a main function and benchmark.

using Nemo, Base.Threads

# CHUNK_SIZE is the size of the data ranges that will be computed one
# at a time. If the program is terminated the progress will fall back
# on the last completed chunk.
const CHUNK_SIZE::ZZRingElem = ZZ(10)^5

# this is the number of cases that will be computed in a given pass of test_range
# used to allow exclusion of ranges based on the computations of form.jl
const RANGE_UNROLL_COUNT::ZZRingElem = ZZ(256)

# This regex reperesents 4 unsigned integers seperated by commas e.g. 1234,65324,2,2345 or 1,0,0,5364
const VALID_FILE_REGEX::Regex = r"^[0-9]+(,[0-9]+){2,3}$"

# The number of threads available to this program.
const THREAD_COUNT::ZZRingElem = ZZ(Threads.nthreads())

"""Runs various setup tasks, loads `data_file`, and returns the `current` value and a `Tuple` of chunks to test."""
function setup(data_file::String)::Tuple{ZZRingElem,Tuple{Vararg{ZZRingElemUnitRange}}}
    # Tell Julia to treat SIGINT (user interrupt: "ctrl + c") as a normal exception.
    # This allows it to be handled and for the program to exit gracfully, saving progress.
    Base.exit_on_sigint(false)

    # warn the user if they are using less threads than are avalable.
    if Threads.nthreads() < Sys.CPU_THREADS
        print("WARNING: currently using: $(Threads.nthreads()) threads when: $(Sys.CPU_THREADS) are avalable. ")
        print("Consider using all avalble threads for maximum speed. Run \"")
        # Print the command in red for ease of reading.
        printstyled("set JULIA_NUM_THREADS=8", color = :red)
        print("\" to run julia.exe on 8 threds.\n")
    end

    goal, current = load(data_file)

    # this is the range of numbers that we need to test
    rng = current:goal

    # this expands the edges of the range so that
    rng2 = ((first(rng)+1) ÷ RANGE_UNROLL_COUNT):((last(rng) + RANGE_UNROLL_COUNT-1) ÷ RANGE_UNROLL_COUNT)

    # split the ranges
    ranges = split_range_by_size(rng2, CHUNK_SIZE)

    return (current, ranges)
end

"""Loads the data from `filename` and returns the values of: `goal`, and `current` in a Tuple.
If `all_values` is true then also return the values of: `id`, and `start` in the form (id, start, goal, current)"""
function load(filename::String, all_values::Bool = false)::Tuple{Vararg{ZZRingElem}}
    # look for the file in the same directory as the worker file.
    filename = joinpath(@__DIR__, filename)
    data = read(filename, String)
    result = match(VALID_FILE_REGEX, data)
    if result === nothing
        throw(ErrorException("Invalid data in file: $filename"))
    end
    data = split(data, ",")
    data = parse.(ZZRingElem, data)
    if length(data) == 3
        # add the starting value as the current value if needed.
        push!(data, data[2])
    end

    if all_values
        # id, start, goal, current
        return (data...,)
    else
        # goal, current
        return (data[3],data[4])
    end
end

"""Updates the data at `filename` with the new current_value of `value`."""
function save(filename::String, value::ZZRingElem)::Nothing
    # load the data and update it with our new values.
    data = [load(filename, true)...]
    data[4] = value

    # save the data.
    open(filename, "w") do io
        write(io, "$(data[1]),$(data[2]),$(data[3]),$(data[4])")
    end

    # this is needed to prevent the value of the open block from being returned.
    # Julia returns the last evaluated expression by default so nothing must be
    # returned excplicitly.
    return nothing
end

"""If `number` is the lowest counterexample to the Collatz Conjecture block forever. Otherwise return `nothing`."""
@inline function test(number::ZZRingElem)::Nothing
    init_number::ZZRingElem = number
    while number<init_number
        number = is_even(number) ? (number >> 1) : ((3*number + 1) >> 1)
    end
end

"""Cast `StepRange` or `UnitRange` `r` to `StepRange{ZZRingElem}`."""
function zz_range(r::Union{StepRange, UnitRange, ZZRingElemUnitRange})::StepRange{ZZRingElem}
    return ZZ(first(r)):ZZ(step(r)):ZZ(last(r))
end

"""Splits the given range into chunks of size `size`."""
@inline function split_range_by_size(range::ZZRingElemUnitRange, size::ZZRingElem)::Tuple{Vararg{ZZRingElemUnitRange}}
    # return the ntuple
    ntuple(
        # this is the calculation for the ith item.
        i -> begin
            start_index = first(range) + (i-1)*size
            end_index = min(start_index + (size - 1), last(range))
            start_index:end_index
        end,

        # this is how many items are in the Tuple.
        Int(length(range) ÷ size + (length(range) % size==0 ? 0 : 1))
    )
end

"""Splits the given range into `count` chunks."""
@inline function split_range_by_count(range::ZZRingElemUnitRange, count::ZZRingElem)::Tuple{Vararg{ZZRingElemUnitRange}}
    size = length(range) ÷ count
    extra = length(range) % count

    # return the ntuple
    ntuple(
        # this is the calculation for the ith item.
        i -> begin
            start_index = first(range) + (i - 1)*size + min(i-1, extra)
            end_index = start_index + size - 1 + (i <= extra ? 1 : 0)
            start_index:end_index
        end,

        # this is how many items are in the Tuple.
        Int(count)
    )
end

"""Tests the given unit range of numbers"""
function test_range_unrolled_256(range::ZZRingElemUnitRange)::Nothing
    for index in range
        # see form.jl for the computation of and reason behind these values.

        # 27       (false, (2187, 242))       8                 Any[1, 1, 0, 1, 1, 1, 1, 1]
        # 31       (false, (729, 91))         8                 Any[1, 1, 1, 1, 1, 0, 1, 0]
        # 47       (false, (729, 137))        8                 Any[1, 1, 1, 1, 0, 1, 0, 1]
        # 63       (false, (729, 182))        8                 Any[1, 1, 1, 1, 1, 1, 0, 0]
        # 71       (false, (729, 206))        8                 Any[1, 1, 1, 0, 1, 0, 1, 1]
        # 91       (false, (729, 263))        8                 Any[1, 1, 0, 1, 1, 1, 0, 1]
        # 103      (false, (2187, 890))       8                 Any[1, 1, 1, 0, 1, 1, 1, 1]
        # 111      (false, (729, 319))        8                 Any[1, 1, 1, 1, 0, 1, 1, 0]
        # 127      (false, (2187, 1093))      8                 Any[1, 1, 1, 1, 1, 1, 1, 0]
        # 155      (false, (729, 445))        8                 Any[1, 1, 0, 1, 1, 1, 1, 0]
        # 159      (false, (2187, 1367))      8                 Any[1, 1, 1, 1, 1, 0, 1, 1]
        # 167      (false, (729, 479))        8                 Any[1, 1, 1, 0, 1, 1, 0, 1]
        # 191      (false, (2187, 1640))      8                 Any[1, 1, 1, 1, 1, 1, 0, 1]
        # 207      (false, (729, 593))        8                 Any[1, 1, 1, 1, 0, 0, 1, 1]
        # 223      (false, (729, 638))        8                 Any[1, 1, 1, 1, 1, 0, 0, 1]
        # 231      (false, (729, 661))        8                 Any[1, 1, 1, 0, 1, 1, 1, 0]
        # 239      (false, (2187, 2051))      8                 Any[1, 1, 1, 1, 0, 1, 1, 1]
        # 251      (false, (729, 719))        8                 Any[1, 1, 0, 1, 1, 0, 1, 1]
        # 255      (false, (6561, 6560))      8                 Any[1, 1, 1, 1, 1, 1, 1, 1]

        # TODO: Use the above data for precomputation of the values.
        # all values can be precomputed to a depth of 8. This would be
        # done by unrolling the below loop.

        for i in (27, 31, 47, 63, 71, 91, 103, 111, 127, 155, 159, 167, 191, 207, 223, 231, 239, 251, 255)
            test(index * RANGE_UNROLL_COUNT + i)
        end
    end
end

"""Tests the given chunk using the @threads macro and test_range."""
function test_chunk(chunk::ZZRingElemUnitRange)::Nothing
    # create ranges from the chunk
    ranges = split_range_by_count(chunk, THREAD_COUNT)

    # then test the ranges
    @threads for i in ranges
        test_range_unrolled_256(i)
    end
end

function main()
    # only goal and current are used during the computations so don't load the other values.
    current, chunks = setup("data")

    println("Starting computation...")
    try
        for i in chunks
            #println(i)
            # TODO: test_chunk generates the ranges in-loop. Try pre-generation.
            test_chunk(i)

            # after the chunk has been tested update our
            # current progress to the last tested value.
            # this value has already been verified.
            current = last(i)

            #     vvvvvvvvvvvv This clears the previous line and moves the cursor back to overwrite with the new number.
            print("\e[2K\e[1G" * string(current * RANGE_UNROLL_COUNT))
        end
        println("Computations finished. Please report `data` back to the centeral database.")
    catch err
        if isa(err, InterruptException)
            println("\nUser interrupt detected. Saving progress and quitting...")
        else
            println("\nError: $err was thrown. \n\nSaving progress and re-throwing...")
            save("data", current * RANGE_UNROLL_COUNT)
            throw(err)
        end
    end
    save("data", current * RANGE_UNROLL_COUNT)
end


main()

#using BenchmarkTools
#@btime test_chunk()

# TODO: How to reliably interrupt the program?? SIGINT is not particularily reliable :(