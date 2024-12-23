// NOTE: The limit for the `unsigned long long` type is: 18446744073709551615
// NOTE: The Collatz Conjecture lower limit so far is  : 295000000000000000000

// When the `unsigned long long` limit is exceeded, the numbers will overflow and chaos will ensue.

// TODO: Consider caching numbers. Probably not worth the overhead though.

#include <stdio.h>
#include <omp.h>
#include <gmp.h> // GMP library for arbitrary precision arithmetic

void test(mpz_t num) {
    // make a copy for comparison
    mpz_t init_num;
    mpz_init_set(init_num, num);

    // NOTE: initially num will be of the form 4n + 3

    // the `do {...} while (condition);` syntax removes the initial condition check which is always true in this case.
    do {
        // given that num is odd we should start with 3n + 1
        mpz_mul_ui(num, num, 3);
        mpz_add_ui(num, num, 1);

        // and then divide until odd
        while (mpz_even_p(num)) {
            mpz_divexact_ui(num, num, 2);
        }

        // after this point num should be compared with init_num
    } while (mpz_cmp(num, init_num) >= 0);

    mpz_clear(init_num);
}

int main() {
    omp_set_num_threads(omp_get_max_threads());
    printf("Computing on %d threads...\n", omp_get_max_threads());

    // Arbitrarily large limit
    mpz_t limit;
    mpz_init_set_str(limit, "100000000000", 10); // 10^11
    mpz_divexact_ui(limit, limit, 256); // Divide by 256

    // NOTE: `static` could be replaced with `dynamic` to balance the workload
    // across the threads better but at the cost of scheduling overhead.
    #pragma omp parallel
    {
        mpz_t i, _2187, _729, temp;
        mpz_inits(i, _2187, _729, temp, NULL);

        #pragma omp for schedule(static, 512)
        for (unsigned long long j = 0; j < mpz_get_ui(limit); j++) {
            mpz_set_ui(i, j);

            // 2187 * i
            mpz_mul_ui(_2187, i, 2187);
            // 729 * i
            mpz_mul_ui(_729, i, 729);

            // only these 19 values in every 256 need testing.
            mpz_add_ui(temp, _2187, 242);
            test(temp);
            mpz_add_ui(temp, _729, 91);
            test(temp);
            mpz_add_ui(temp, _729, 137);
            test(temp);
            mpz_add_ui(temp, _729, 182);
            test(temp);
            mpz_add_ui(temp, _729, 206);
            test(temp);
            mpz_add_ui(temp, _729, 263);
            test(temp);
            mpz_add_ui(temp, _2187, 890);
            test(temp);
            mpz_add_ui(temp, _729, 319);
            test(temp);
            mpz_add_ui(temp, _2187, 1093);
            test(temp);
            mpz_add_ui(temp, _729, 445);
            test(temp);
            mpz_add_ui(temp, _2187, 1367);
            test(temp);
            mpz_add_ui(temp, _729, 479);
            test(temp);
            mpz_add_ui(temp, _2187, 1640);
            test(temp);
            mpz_add_ui(temp, _729, 593);
            test(temp);
            mpz_add_ui(temp, _729, 638);
            test(temp);
            mpz_add_ui(temp, _729, 661);
            test(temp);
            mpz_add_ui(temp, _2187, 2051);
            test(temp);
            mpz_add_ui(temp, _729, 719);
            test(temp);
            mpz_mul_ui(temp, i, 6561);
            mpz_add_ui(temp, temp, 6560);
            test(temp);
        }

        mpz_clears(i, _2187, _729, temp, NULL);
    }

    mpz_clear(limit);
    return 0;
}

// use -fopt-info-vec for information on loop vectorisation.
// the `-march=native` means to compile for my specific CPU. Remove this flag for a more general exe
// replace `main` with `main.exe` for windows.

// gcc -O3 -fopenmp -flto -ftree-vectorize -lgmp -march=native main.c -o main