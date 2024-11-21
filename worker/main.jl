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


# TODO: Benchmark out-of-loop precomputation of the first two 1.5n+1 steps and passing in both values vs computing in function.

# TODO: Try putting all the below into a main function and benchmark.



#region tools
"""Functions to create, steralise, load, save and compute various test ranges."""
module Tools

export setup, test_chunk, save

using Nemo, Base.Threads

# CHUNK_SIZE is the size of the data ranges that will be computed one
# at a time. If the program is terminated the progress will fall back
# on the last completed chunk.
const CHUNK_SIZE::ZZRingElem = ZZ(10)^7

# this is the number of cases that will be computed in a given pass of test_range
# used to allow exclusion of ranges based on the computations of form.jl
const RANGE_UNROLL_COUNT::ZZRingElem = ZZ(256)

# This regex reperesents 4 unsigned integers seperated by commas e.g. 1234,65324,2,2345 or 1,0,0,5364
const VALID_FILE_REGEX::Regex = r"^[0-9]+(,[0-9]+){2,3}$"

# The number of threads available to this program.
const THREAD_COUNT::Int = Threads.nthreads()

"""Runs various setup tasks, loads `data_file`, and returns the `current` value and a `Tuple` of chunks to test."""
function setup(data_file::String)::Tuple{ZZRingElem,Tuple{Vararg{StepRange{ZZRingElem}}}}
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

    # the current value has already been computed so go to the next one.
    chunks = generate_chunks(zz_range(current+1 : goal))

    return (current, chunks)
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
    number = ((3*((3*number + 1) >> 1) + 1) >> 1) # TODO: expand and simpify.
    while number<init_number
        number = is_even(number) ? (number >> 1) : ((3*number + 1) >> 1)
    end
end

"""Cast `StepRange` or `UnitRange` `r` to `StepRange{ZZRingElem}`."""
function zz_range(r::Union{StepRange, UnitRange, ZZRingElemUnitRange})::StepRange{ZZRingElem}
    return ZZ(first(r)):ZZ(step(r)):ZZ(last(r))
end

# neither `split_range` or `split_range_8` need to account for the various edge cases such as
# 0 width ranges or other strange inputs as all inputs come steralised from other functions.

"""Split range `r` into `n` parts in round-robin fashion and return the parts in a `Tuple`."""
@inline function split_range(r::StepRange{ZZRingElem}, n::Integer)::Tuple{Vararg{StepRange{ZZRingElem}}}
    first_r = first(r)
    step_r  = step(r)

    # this is the number of steps that r will take to finish i.e. the number of iterations that would occour when looping over it.
    steps_taken = (last(r)-first_r)/step(r) + 1 # because both ends inclusive

    # some values that don't change accross loop iterations and so are precomputed here:
    new_step = 8 * step_r
    base_steps = steps_taken ÷ 8 -1
    #            ^^^^^^^^^^^^^^^ already floored due to integer division.
    steps_taken_mod_n = steps_taken % 8

    parts = ntuple(i -> begin
        # This block is the function used to evaluate the items of the NTuple. `i` is an argument reperesenting the index starting at 1.
        new_start= first_r + (i - 1)*step_r
        new_stop = new_start + new_step * (base_steps + (steps_taken_mod_n > (i - 1) ? 1 : 0))
        new_start:new_step:new_stop
    end, n)

    return parts
end

"""Generate and return `threads` number of valid search ranges that ensure that `range` is fully covered."""
@inline function generate_ranges(range::StepRange{ZZRingElem}, threads::Int)::Tuple{Vararg{StepRange{ZZRingElem}}}
    # formula to find closest number of form 4n + 3: 3, 7, 11, 15, 19, 23, 27
    # n-(n-3)%4 is rounded down
    # n+(3-n%4)%4 is rounded up
    # ensure that all numbers in range are of the form 4n + 3 by setting the step to 4 and moving the ends inwards.
    r_first = first(range)
    r_last  = last(range)
    range = r_first+(3-r_first%4)%4 : ZZ(4) : r_last-(r_last-3)%4

    # distribute the numbers accorss the provided threads ans return.
    split_range(range, threads)
end

"""Splits the given range into chunks of size `chunk_size`."""
@inline function generate_chunks(range::StepRange{ZZRingElem}, chunk_size::ZZRingElem = CHUNK_SIZE)::Tuple{Vararg{StepRange{ZZRingElem}}}
    # return the ntuple
    ntuple(
        # This is the calculation for the ith item.
        i -> begin
            # see split_range for an explination of this syntax.
            start_index = first(range) + (i-1)*chunk_size*step(range)
            end_index = min(start_index + (chunk_size - 1)*step(range), last(range))
            start_index:step(range):end_index
        end,

        # This is how many items are in the Tuple.
        Int(length(range) ÷ chunk_size + (length(range)%chunk_size!=0 ? 1 : 0))
    )
end

"""run `test` on all numbers in the given range."""
function test_range(range::StepRange{ZZRingElem})::Nothing
    for number in range
        test(number)
    end
end

function test_range_unrolled_256(range::StepRange{ZZRingElem})::Nothing
    # here range is expected to be every 256th valid search number.
    for number in range
        for i in (27, 31, 47, 63, 71, 91, 103, 111, 127, 155, 159, 167, 191, 207, 223, 231, 239, 251, 255)
            test(number + 4 * i)
        end
    end
end

"""Tests the given chunk using the @threads macro and test_range."""
function test_chunk(chunk::StepRange{ZZRingElem})::Nothing
    # create ranges from the chunk
    ranges = generate_ranges(chunk, THREAD_COUNT)

    # then test the ranges
    @threads for i in ranges
        test_range(i)
    end
end

end
#endregion


using .Tools

# only goal and current are used during the computations so don't load the other values.
current, chunks = setup("data")

println("Starting computation...")
try
    for i in chunks
        # TODO: test_chunk generates the ranges in-loop. Try pre-generation.
        test_chunk(i)

        # after the chunk has been tested update our
        # current progress to the last tested value.
        # this value has already been verified.
        global current = last(i)

        #      vvvvvvvvvvvv This clears the previous line and moves the cursor back to overwrite with the new number.
        print("\e[2K\e[1G"*string(current))
    end
    println("Computations finished. Please report `data` back to the centeral database.")
catch err
    if isa(err, InterruptException)
        println("\nUser interrupt detected. Saving progress and quitting...")
    else
        println("\nError: $err was thrown. Saving progress and re-throwing...")
        save("data", current)
        throw(err)
    end
end
save("data", current)


# TODO: How to reliably interrupt the program?? SIGINT is not particularily reliable :(