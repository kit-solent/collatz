#include <stdio.h>
#include <omp.h>
#include <gmp.h> // NOTE: given that my code is compiled and run through WSL this error is not a problem.

int main() {
    omp_set_num_threads(omp_get_max_threads());
    printf("Computing on %d threads...\n", omp_get_max_threads());

    // 10^11, gcc will precompute the division.
    mpz_t limit, i;
    mpz_init_set_str(limit, "10000000000", 10); // 10^10
    mpz_init(i);

    #pragma omp parallel
    {
        mpz_t local_i;
        mpz_init(local_i);

        #pragma omp for schedule(static, 512)
        for (unsigned long long j = 0; j < mpz_get_ui(limit); j++) {
            mpz_set_ui(local_i, j);
            // Perform some computation with local_i
            // Example: 2 + 2 (this is just a placeholder, replace with actual computation)
            mpz_add_ui(local_i, local_i, 2);
        }

        mpz_clear(local_i);
    }

    gmp_printf("limit: %Zd\n", limit);
    mpz_clear(limit);
    mpz_clear(i);

    return 0;
}

// gcc -O3 -fopenmp -flto -ftree-vectorize -march=native speedyweedy.c -lgmp -o speedyweedy