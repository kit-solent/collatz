// NOTE: The limit for the `unsigned long long` type is: 18446744073709551615
// NOTE: The Collatz Conjecture lower limit so far is  : 295000000000000000000

// When the `unsigned long long` limit is exceded the numbers will overflow and chaos will ensue.

// TODO: Consider caching numbers. Probably not worth the overhead though.


#include <stdio.h>
#include <omp.h>
#include <gmp.h> // NOTE: given that my code is compiled and run through WSL this error is not a problem.


inline void test(unsigned long long num) {
    // make a copy for comparison
    unsigned long long init_num = num;

    // NOTE: initially num will be of the form 4n + 3

    // the `do {...} while (condition);` syntax removes the initial condition check which is always true in this case.
    do {
        // given that num is odd we should start with 3n + 1
        // NOTE: this step could be performed in binary with: `num = ((num << 1) | 1) + num;`
        // but due to compiler optimisations would probably have no effect and could even be
        // slower due to modern CPU multiplication methods.
        num = 3*num + 1;

        // and then divide untill odd.
        num >>= __builtin_ctzll(num);

        // after this point num should be compared with init_num

        // NOTE: unrolling more iterations could lead to the number
        // climbing again and taking longer to fall so don't do that.
    } while (num >= init_num);
}

int main() {
    omp_set_num_threads(omp_get_max_threads());
    printf("Computing on %d threads...\n", omp_get_max_threads());

    // 10^11, gcc will precompute the division.
    const unsigned long long limit = 100000000000ULL / 256;
    // NOTE: the limit is divided by 256 as we are incrementing our loop by 1 rather than 256.
    // each loop iteration tests the required 19 values for it's 256 value chunk. This means
    // we can use floor division to calculate the limit without missing values.

    // NOTE: `static` could be replaced with `dynamic` to balence the workload
    // accross the threads better but at the cost of scheduling overhead.
    #pragma omp parallel for schedule(static, 512)
    for (unsigned long long i = 0; i < limit; i++) {
        // see simple.py for the algorithm behind these test values.
        // NOTE: (i << 8) has been replaced with i as we are incrementing out loop by 1 rather than 256.

        // NOTE: interesting fact:
        // 729  = 3^6
        // 2187 = 3^7
        // 6561 = 3^8
        unsigned long long _2187 = 2187*i;
        unsigned long long _729 = 729*i;

        // only these 19 values in every 256 need testing.
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
        test(6561*i + 6560);
    }

    return 0;
}

// use -fopt-info-vec for information on loop vectorisation.
// the `-march=native` means to compile for my specific CPU. Remove this flag for a more general exe
// replace `main` with `main.exe` for windows.

// gcc -O3 -fopenmp -flto -ftree-vectorize -lgmp -march=native main.c -o main