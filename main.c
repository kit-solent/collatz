// NOTE: The limit for the `unsigned __int128` type is: 340282366920938463463374607431768211455
// NOTE: The Collatz Conjecture lower limit so far is : 295147905179352825856
// NOTE: While overflow could occour when testing higher values the unsigned __int128 limit is probably high enough.

#include <stdio.h>
#include <omp.h>

int main() {
    const unsigned __int128 limit = (unsigned __int128)10000000000 * 10 / 256;
    printf("Haha: %d", limit);
    printf("Haha: %d", __builtin_ctz(limit));

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