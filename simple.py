
def will_fall(a:int, b:int):
    # copy the variables
    x, y = a, b

    while True:
        if x % 2 == 0:
            if y % 2 == 0:
                x /= 2
                y /= 2

                if x < a or (x == a and y < b):
                    return True
            else:
                x = (3*x) / 2
                y = ...

for i in range(256):
    pass