// NOTE: The limit for the `unsigned long long` type is: 18446744073709551615
// NOTE: The Collatz Conjecture lower limit so far is  : 295000000000000000000

// When the `unsigned long long` limit is exceded the numbers will overflow and chaos will ensue.

// TODO: Consider caching numbers. Probably not worth the overhead though.


#include <stdio.h>
#include <omp.h>
#include <gmp.h> // TODO: get GMP working.


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

    const unsigned long long limit = 100000000ULL * 256; // 10^8, gcc will precompute the multiplication.

    // NOTE: `static` could be replaced with `dynamic` to balence the workload
    // accross the threads better but at the cost of scheduling overhead.
    #pragma omp parallel for schedule(static, 512)
    for (unsigned long long i = 0; i < limit; i++) {
        // see simple.py for the algorithm behind these results. Collumns are: form, result, transform, test value, simplifications, etc...
        //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        // 256n + 27       2187n + 242     (2187/256)n + 2903/256  (2187/256)*(i + 27) + 2903/256  (2187/256)*i + 242      2187*(i >> 8) + 242
        // 256n + 31       729n + 91       (729/256)n + 697/256    (729/256)*(i + 31) + 697/256    (729/256)*i + 91        729*(i >> 8) + 91
        // 256n + 47       729n + 137      (729/256)n + 809/256    (729/256)*(i + 47) + 809/256    (729/256)*i + 137       729*(i >> 8) + 137
        // 256n + 63       729n + 182      (729/256)n + 665/256    (729/256)*(i + 63) + 665/256    (729/256)*i + 182       729*(i >> 8) + 182
        // 256n + 71       729n + 206      (729/256)n + 977/256    (729/256)*(i + 71) + 977/256    (729/256)*i + 206       729*(i >> 8) + 206
        // 256n + 91       729n + 263      (729/256)n + 989/256    (729/256)*(i + 91) + 989/256    (729/256)*i + 263       729*(i >> 8) + 263
        // 256n + 103      2187n + 890     (2187/256)n + 2579/256  (2187/256)*(i + 103) + 2579/256 (2187/256)*i + 890      2187*(i >> 8) + 890
        // 256n + 111      729n + 319      (729/256)n + 745/256    (729/256)*(i + 111) + 745/256   (729/256)*i + 319       729*(i >> 8) + 319
        // 256n + 127      2187n + 1093    (2187/256)n + 2059/256  (2187/256)*(i + 127) + 2059/256 (2187/256)*i + 1093     2187*(i >> 8) + 1093
        // 256n + 155      729n + 445      (729/256)n + 925/256    (729/256)*(i + 155) + 925/256   (729/256)*i + 445       729*(i >> 8) + 445
        // 256n + 159      2187n + 1367    (2187/256)n + 2219/256  (2187/256)*(i + 159) + 2219/256 (2187/256)*i + 1367     2187*(i >> 8) + 1367
        // 256n + 167      729n + 479      (729/256)n + 881/256    (729/256)*(i + 167) + 881/256   (729/256)*i + 479       729*(i >> 8) + 479
        // 256n + 191      2187n + 1640    (2187/256)n + 2123/256  (2187/256)*(i + 191) + 2123/256 (2187/256)*i + 1640     2187*(i >> 8) + 1640
        // 256n + 207      729n + 593      (729/256)n + 905/256    (729/256)*(i + 207) + 905/256   (729/256)*i + 593       729*(i >> 8) + 593
        // 256n + 223      729n + 638      (729/256)n + 761/256    (729/256)*(i + 223) + 761/256   (729/256)*i + 638       729*(i >> 8) + 638
        // 256n + 231      729n + 661      (729/256)n + 817/256    (729/256)*(i + 231) + 817/256   (729/256)*i + 661       729*(i >> 8) + 661
        // 256n + 239      2187n + 2051    (2187/256)n + 2363/256  (2187/256)*(i + 239) + 2363/256 (2187/256)*i + 2051     2187*(i >> 8) + 2051
        // 256n + 251      729n + 719      (729/256)n + 1085/256   (729/256)*(i + 251) + 1085/256  (729/256)*i + 719       729*(i >> 8) + 719
        // 256n + 255      6561n + 6560    (6561/256)n + 6305/256  (6561/256)*(i + 255) + 6305/256 (6561/256)*i + 6560     6561*(i >> 8) + 6560
        //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

        // only these 19 values in every 256 need testing.

        // NOTE: interesting fact:
        // 729  = 3^6
        // 2187 = 3^7
        // 6561 = 3^8
        unsigned long long _2187 = 2187*i;
        unsigned long long _729 = 729*i;

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