# calculates general numbers e.g. numbers of the form an + b

# TODO: We are not using nemo as the numbers should never get that big but if they do then
# switch to ZZRingElem in place of Int

"""Computes the given form: `a`n + `b`. Returns true if the form falls and the form at which it has fallen.
Returns false if its parity becomes unknown and the point at which that happens."""
function compute_form(a::Int, b::Int)::Tuple{Bool, Tuple{Int, Int}}
    # copy the initial values for reference.
    x, y = a, b
    while true
        if iseven(x)
            if iseven(y)
                # if both a and b are even then the number is even so halve it
                # (an + b) ÷ 2 = (a÷2)n + (b÷2)
                x ÷= 2
                y ÷= 2

                if x < a || (x == a && y < b)
                    # if the a value drops then return the value where it is below the starting value
                    # if a is smaller but b is much larger then small values of n will not fall below
                    # their starting values. This does however allow for the computation of an upper limit
                    # for counterexample numbers of the given form.
                    return true, (x, y)
                end
            elseif isodd(y)
                # this step will always increase the value of the form so checking for falling below starting values is not needed

                # if a is even and b is odd then the number is odd so apply (3x + 1) ÷ 2
                # (3(an + b) + 1) ÷ 2 = 1.5(an + b) + 0.5 = (1.5a)n + (1.5b + 0.5)

                # divide by 2 before tripling to reduce the intermediate values. i.e. trippling first will lead to a larger
                # value before halving so is more computationally expensive.
                x = 3*(x ÷ 2) # overall a = (3a) ÷ 2 = 1.5a
                y = (3*y + 1) ÷ 2 # this will remain an integer because b is odd and 3n + 1 flips parity.
            end
        else
            # if a is odd then a*n will have an inconstant parity and therfore so will a*n + b
            # this means that the parity of the form is inconstant
            return false, (x, y) # return the point at which the parity became unknown
        end
    end
end

function split_form(form::Tuple{Int, Int}, parts::Int)::Tuple{Vararg{Tuple{Int, Int}}}
    ntuple(i -> begin (form[1]*parts, form[2] + form[1]*(i-1)) end, parts)
end

"""A recursive algorithm for computing forms to a given depth"""
function compute_form_step(form::Tuple{Int, Int}, depth::Int, split::Int)
    println(form)
    println(depth)
    println(split)
    println("\n")
    if depth <= 0
        # if the depth is 0 then stop computing.
        # return an empty fallen_forms and the given form
        return ([], [form])
    end
    # a temporary looping variable
    new_forms = []

    # holds the forms that are known to fall
    fallen_forms = []

    result = compute_form(form[1], form[2])
    println(result)
    println([(form, result[2])])
    if result[1]
        # if the result falls then add the form and fall point to the fallen_forms
        fallen_forms += [(form, result[2])]
    else
        # otherwise the forms parity becomes unknown so split the form
        split_result = split_form(result[2], split)

        # for all parts of the split perform compute_form_step on them and record the results.
        for i in split_result
            println(i)
            println()
            result = compute_form_step(i, depth-1, split)
            # add the fallen forms and new forms to our arrays.
            fallen_forms += result[1]
            new_forms += result[2]
        end
    end

    return (fallen_forms, new_forms)
end

compute_form_step((1, 0), 4, 2)