import main

print("-- Calculation 1: Forms that don't fall and their precomputations. --")
# obtain a list of all forms 256n + k that don't fall below their starting value where k ranges from 0 to 255.
# together, these forms cover all natural numbers that don't fall.
results = main.Form.compute_set(256, filter_fallen=True)
for count, result in enumerate(results, 1):
    print(f"{str(count).rjust(3)}) {result.start} \t({result.steps})->\t {result.end}")

print("\nThis means that for every chunk of 256 numbers i.e. numbers of the form 256n + k where k ranges from 0 to 255, \
there are only 19 values that don't fall below their starting value and these values can be precomputed 14 or 15 steps.")




##NOTE: Interesting pattern #1
# this shows that for every chunk of numbers of the form 256n + k where k ranges from 0 to 255
# there are only 19 values that don't fall below their starting value and, when these values are
# precomputed the a values of the resulting forms an + b are all powers of 3 (3^6, 3^7, and in just the last case 3^8)
# for i, result in enumerate(main.Form.compute_set(256, filter_fallen=True), 1):
    # print(f"{math.log(result.end.a, 3)}")


