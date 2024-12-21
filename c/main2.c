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

    // 10^11
    const unsigned long long limit = 100000000000ULL;

    // NOTE: `static` could be replaced with `dynamic` to balence the workload
    // accross the threads better but at the cost of scheduling overhead.
    #pragma omp parallel for schedule(static, 512)
    for (unsigned long long i = 3; i < limit; i+=4) {
        test(i);
    }

    return 0;
}

// use -fopt-info-vec for information on loop vectorisation.
// the `-march=native` means to compile for my specific CPU. Remove this flag for a more general exe
// replace `main` with `main.exe` for windows.

// gcc -O3 -fopenmp -flto -ftree-vectorize -lgmp -march=native main.c -o main