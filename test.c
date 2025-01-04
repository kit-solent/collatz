// NOTE: The limit for the `unsigned __int128` type is: 340282366920938463463374607431768211455
// NOTE: The Collatz Conjecture lower limit so far is : 295147905179352825856
// NOTE: While overflow could occour when testing higher values the unsigned __int128 limit is probably high enough.

#include <stdio.h>
#include <omp.h>

void print_uint128(unsigned __int128 value) {
    // Split the 128-bit value into two 64-bit parts
    unsigned long long high = value >> 64;
    unsigned long long low = value & 0xFFFFFFFFFFFFFFFF;

    // Print the value
    if (high == 0) {
        printf("%llu\n", low);
    } else {
        printf("%llu%018llu\n", high, low);
    }
}

int main() {
    const unsigned __int128 limit = (unsigned __int128)10000000000 * 1000000000;
    printf("Limit: ");
    print_uint128(limit);
    printf("\nctz: %d\n", __builtin_ctz(limit));

    return 0;
}

// gcc -O3 -fopenmp -flto -ftree-vectorize -m64 -march=native test.c -o test