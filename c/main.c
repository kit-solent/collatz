// NOTE: The limit for the `unsigned __int128` type is: 340282366920938463463374607431768211455
// NOTE: The Collatz Conjecture lower limit so far is : 295147905179352825856
// NOTE: While overflow could occur when testing higher values the unsigned __int128 limit is probably high enough.

#include <stdio.h>
#include <omp.h>

inline int ctz_128(unsigned __int128 num) {
    // extract the lower 64 bits by casting directly.
    unsigned long long lo = (unsigned long long)num;
    // use a right shift to extract the upper 64 bits.
    unsigned long long hi = (unsigned long long)(num >> 64);

    if (lo == 0) return __builtin_ctzll(hi) + 64;

    return __builtin_ctzll(lo);
}

// inline may not be needed here.
inline void test(unsigned __int128 num) {
    // make a copy for comparison
    unsigned __int128 init_num = num;

    // NOTE: Due to precomputation, the initial form and parity of the numbers are unknown.

    num >>= ctz_128(num); // ensure that num starts odd.

    while (num >= init_num) {
        // given that num is odd we should start with 3n + 1
        num = 3 * num + 1;

        // and then divide until odd using a right shift by the number of trailing 0s.
        num >>= ctz_128(num);

        // after this point num should be compared with init_num

        // NOTE: unrolling more iterations could lead to the number
        // climbing again and taking longer to fall so don't do that.
    }
}

int main() {
    // OpenMP uses all available threads by default.
    // The number of threads can be controlled using the OMP_NUM_THREADS environment variable.
    printf("Computing on %d threads...\n", omp_get_max_threads());

    // 10^11, gcc will precompute the division.
    // the first chunk ((unsigned __int128)10000000000 = 10^10) is the only one that needs the type cast.
    // the rest of the expression will be automatically promoted to __int128.
    const unsigned __int128 limit = (unsigned __int128)10000000000 * 10 / 256;
    // NOTE: the limit is divided by 256 as we are incrementing our loop by 1 rather than 256.
    // each loop iteration tests the required 19 values for its 256 value chunk. This means
    // we can use floor division to calculate the limit without missing values.

    // NOTE: `static` could be replaced with `dynamic` to balance the workload
    // across the threads better but at the cost of scheduling overhead.
    #pragma omp parallel for schedule(static)
    for (unsigned __int128 i = 0; i < limit; i++) {
        // see simple.py for the algorithm behind these test values.
        // NOTE: (i << 8) has been replaced with i as we are incrementing our loop by 1 rather than 256.

        unsigned __int128 _2187 = 2187 * i;
        unsigned __int128 _729 = 729 * i;

        test(_2187 + 242);
        test(_729 + 91);
        test(_729 + 137);
        test(_729 + 182);
        test(_729 + 206);
        test(_729 + 263);
        test(_2187 + 890);
        test(_729 + 319);
        test(_2187 + 1093);
        test(_729 + 445);
        test(_2187 + 1367);
        test(_729 + 479);
        test(_2187 + 1640);
        test(_729 + 593);
        test(_729 + 638);
        test(_729 + 661);
        test(_2187 + 2051);
        test(_729 + 719);
        test(6561 * i + 6560);
    }

    return 0;
}

// gcc -O3 -fopenmp -flto -ftree-vectorize -m64 -march=native main.c -o main

// "#" = not included.
// -O3 is the flag for the highest optimisation level.
//# -static means to bundle the required libraries into the executable.
// -fopenmp is the flag for OpenMP support.
// -flto is the flag for link time optimisation.
// -ftree-vectorize is the flag for loop vectorisation.
// -m64 is the flag to compile for 64 bit.

// -march=native is the flag to compile for the specific CPU. Remove this for a more general executable.

// main.c is the target file
// -o main is the output file, replace "main" with "main.exe" when running on windows.