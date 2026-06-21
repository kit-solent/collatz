import main

print("-- Calculation 1: Forms 256n + k that don't fall and their precomputations. --")
# obtain a list of all forms 256n + k where k ranges from 0 to 255, that don't fall below their starting value.
# together, these forms cover all natural numbers that don't fall.
results = main.Form.compute_set(256, filter_fallen=True)
for count, result in enumerate(results, 1):
    print(f"{str(count).rjust(3)}) {result.start} \t({result.steps})->\t {result.end}")

print("\nThis means that for every chunk of 256 numbers i.e. numbers of the form 256n + k where k ranges from 0 to 255, \
there are only 19 values that don't fall below their starting value and these values can be precomputed 14 or 15 steps. 19/256 ≈ 7.42%")

print("\n\n\n")
print("-- Calculation 2: Ratios for precomputation --")
print("Commented out because it's 100 lines")
#for i in range(1, 101):
#    results = main.Form.compute_set(i, filter_fallen=True)
#    print(f"{str(i).rjust(3)}) {len(results)*100/i}%")

print("\nSome very power-of-2-ish patterns going on here.")

print("\n\n\n")
print("-- Calculation 3: Ratios for precomputation for powers of 2 --")
for i in range(1, 19):
    results = main.Form.compute_set(2**i, filter_fallen=True)
    num=f"2^{i} = {2**i}"
    print(f"{num.rjust(13)})\t{len(results)}/{2**i} = {len(results)*100/2**i}%")

print("\nA076227")

# 2^16 gives ~3%


##NOTE: Interesting pattern #1
# this shows that for every chunk of numbers of the form 256n + k where k ranges from 0 to 255
# there are only 19 values that don't fall below their starting value and, when these values are
# precomputed the a values of the resulting forms an + b are all powers of 3 (3^6, 3^7, and in just the last case 3^8)
# for i, result in enumerate(main.Form.compute_set(256, filter_fallen=True), 1):
    # print(f"{math.log(result.end.a, 3)}")


