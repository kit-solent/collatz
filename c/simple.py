import math
from fractions import Fraction as f

def will_fall(a:f, b:f):
    # copy the variables
    x, y = a, b

    data = [
        [a, b], # form
        [f(1), f(0)], # result
        [f(1), f(0)], # transform
    ]

    while True:
        data[1] = [x, y]
        if x % 2 == 0:
            if y % 2 == 0:
                # if both x and y are even then xn + y is even so halve both of them.
                x /= 2
                data[2][0] /= 2
                y /= 2
                data[2][1] /= 2

                if x < a or (x == a and y < b):
                    return (True, data)
            else:
                # if x is even and y is odd then xn + y is odd so apply (3n + 1)/2
                # (3(xn + y) + 1)/2 = (3x/2)n + (3y + 1)/2
                x = (3*x) / 2
                data[2][0] = (3*data[2][0]) / 2
                y = (3*y + 1) / 2
                data[2][1] = (3*data[2][1] + 1) / 2
        else:
            return (False, data)


def nice_fraction(fraction:f):
    try:
        fraction = f(fraction)
    except BaseException as err:
        print(f"OOPSIES: {err}")

    return f"{fraction.numerator}" + (f"/{fraction.denominator}" if fraction.denominator > 1 else "")






collumns = "{:<15}{:<15}{:<26}{:<35}{:<24}{:<30}"

# Print headers with fixed-width fields
print(collumns.format("form", "result", "transform", "test", "value", "simplification"))

for i in range(256):
    x = will_fall(256, f(i))
    if not x[0]:
        form = f"{x[1][0][0]}n + {x[1][0][1]}"
        result = f"{nice_fraction(x[1][1][0])}n + {nice_fraction(x[1][1][1])}"
        transform = f"({nice_fraction(x[1][2][0])})n + {nice_fraction(x[1][2][1])}"
        test = f"({nice_fraction(x[1][2][0])})*(i + {x[1][0][1]}) + {nice_fraction(x[1][2][1])}"
        value = f"({nice_fraction(x[1][2][0])})*i + {nice_fraction(x[1][2][0] * x[1][0][1] + x[1][2][1])}"
        simplification = f"{x[1][2][0].numerator}*(i >> 8) + {nice_fraction(x[1][2][0] * x[1][0][1] + x[1][2][1])}" if x[1][2][0].denominator == 256 else ""

        # Print each row with fixed-width fields
        print(collumns.format(form, result, transform, test, value, simplification))