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
function compute_form_step(form::Tuple{Int, Int}, depth::Int, split::Int)::Tuple{Vector{Tuple{Tuple{Int, Int}, Tuple{Int, Int}}}, Vector{Tuple{Int, Int}}}
    # a temporary looping variable
    new_forms = Vector{Tuple{Int, Int}}()

    # holds the forms that are known to fall
    fallen_forms = Vector{Tuple{Tuple{Int, Int}, Tuple{Int, Int}}}()

    parity_result = compute_form(form[1], form[2])
    if depth <= 0
        # if the depth is 0 then stop computing.
        # return an empty fallen_forms and the given form
        push!(new_forms, form)
    elseif parity_result[1]
        # if the result falls then add the form and fall point to the fallen_forms
        push!(fallen_forms, (form, parity_result[2]))
    else
        # otherwise the forms parity becomes unknown so split the form
        # TODO: splitting the result of the parity calculation (parity_result[2]) would mean we are now considering a transformation on
        # our origonal form. This leads to double ups of fallen_forms like 2, 0 and 4, 2 or 4, 0 both of which are sub-forms.
        # it would be worth considering the implications of splitting various forms.
        split_result = split_form(form, split)
        # for all parts of the split perform compute_form_step on them and record the results.
        for i in split_result
            result = compute_form_step(i, depth-1, split)
            # add the fallen forms and new forms to our arrays.
            append!(fallen_forms, result[1])
            append!(new_forms, result[2])
        end
    end
    return (fallen_forms, new_forms)
end

println(compute_form_step((1, 0), 10, 2)[1])


((2, 0), (1, 0)),
((4, 1), (3, 1)),
((16, 3), (9, 2)),
((32, 11), (27, 10)),
((32, 23), (27, 20)),

((128, 7), (81, 5)),
((128, 15), (81, 10)),
((128, 59), (81, 38)),

((256, 39), (243, 38)),
((256, 79), (243, 76)),
((256, 95), (243, 91)),
((256, 123), (243, 118)),
((256, 175), (243, 167)),
((256, 199), (243, 190)),
((256, 219), (243, 209))