using Base.Threads

# Returns the nth linear equation.
# This is done by converting n into
# binary and halving on a 1 and
# 3x+1 ing on a 0
@inline function equation(n::UInt)
    coef = 1
    con  = 0
    for i in digits(n,base=2)
        if Bool(i)
            # 1 reperesents even so halve both values
            coef /= 2
            con  /= 2
        else
            # 0 reperesents odd so (3x+1)/2
            coef *= 1.5
            con = 1.5*con + 0.5
        end
    end

    # we now have a simplified linear equation reperesenting the
    # steps performed on number x in the form ax+b

    # since ax + b = x is our solution (if an integer)
    # where a = coef and b = con
    num = con/(1-coef)
    if isinteger(num) && num>4 # because 1, 2, and 4 all go back to themselvs
        return true
    else
        return false
    end
end

println("Starting...")
@threads for i::UInt in 0:2^30
    if equation(i)
        println(i)
    end
end

# Eliahou proved that the period of a non-trivial cycle must
# be in the form: p = 301994a + 17087915b + 85137581c where
# b >= 1 and ac = 0
# The lower limit for this period is known to be:
# 114,208,327,604
# (using the shortcut where 3x+1 and x/2 are one step.)