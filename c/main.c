#include <stdio.h>
#include <omp.h>

inline void test(unsigned long long num) {
    // make a copy for comparison
    unsigned long long init_num = num;

    // NOTE: num will be of the form 4n + 3 and so will be odd

    // the `do {...} while (condition);` syntax removes the initial condition check which is always true in this case.
    do {
        // given that num is odd we should start with 3n + 1
        // NOTE: this step could be performed in binary with: `num = ((num << 1) | 1) + num;`
        // but due to compiler optimisations would probably have no effect and could even be
        // slower due to modern CPU multiplication methods.
        num = 3*num + 1;

        // and then divide untill odd.
        num = num & -num;

        // after this point num should be compared with init_num

        // NOTE: unrolling more iterations could lead to the number
        // climbing again and taking longer to fall so don't do that.
    } while (num >= init_num);
}

int main() {
    omp_set_num_threads(omp_get_max_threads());
    printf("Computing on %d threads...\n", omp_get_max_threads());

    const unsigned long long limit = 1000000000000; // 10^12

    #pragma omp parallel for schedule(dynamic, 1024)
    for (unsigned long long i = 0; i < limit; i+=256) {
        // see simple.py for the algorithm behind these results. Collumns are: form, result, transform, test value.
        //////////////////////////////////////////////////////////////////////////////////////////////
        // 256n + 27       2187n + 242     (2187/256)n + 2903/256  (2187*(i + 27) + 2903) / 256
        // 256n + 31       729n + 91       (729/256)n + 697/256    (729*(i + 31) + 697) / 256
        // 256n + 47       729n + 137      (729/256)n + 809/256    (729*(i + 47) + 809) / 256
        // 256n + 63       729n + 182      (729/256)n + 665/256    (729*(i + 63) + 665) / 256
        // 256n + 71       729n + 206      (729/256)n + 977/256    (729*(i + 71) + 977) / 256
        // 256n + 91       729n + 263      (729/256)n + 989/256    (729*(i + 91) + 989) / 256
        // 256n + 103      2187n + 890     (2187/256)n + 2579/256  (2187*(i + 103) + 2579) / 256
        // 256n + 111      729n + 319      (729/256)n + 745/256    (729*(i + 111) + 745) / 256
        // 256n + 127      2187n + 1093    (2187/256)n + 2059/256  (2187*(i + 127) + 2059) / 256
        // 256n + 155      729n + 445      (729/256)n + 925/256    (729*(i + 155) + 925) / 256
        // 256n + 159      2187n + 1367    (2187/256)n + 2219/256  (2187*(i + 159) + 2219) / 256
        // 256n + 167      729n + 479      (729/256)n + 881/256    (729*(i + 167) + 881) / 256
        // 256n + 191      2187n + 1640    (2187/256)n + 2123/256  (2187*(i + 191) + 2123) / 256
        // 256n + 207      729n + 593      (729/256)n + 905/256    (729*(i + 207) + 905) / 256
        // 256n + 223      729n + 638      (729/256)n + 761/256    (729*(i + 223) + 761) / 256
        // 256n + 231      729n + 661      (729/256)n + 817/256    (729*(i + 231) + 817) / 256
        // 256n + 239      2187n + 2051    (2187/256)n + 2363/256  (2187*(i + 239) + 2363) / 256
        // 256n + 251      729n + 719      (729/256)n + 1085/256   (729*(i + 251) + 1085) / 256
        // 256n + 255      6561n + 6560    (6561/256)n + 6305/256  (6561*(i + 255) + 6305) / 256
        //////////////////////////////////////////////////////////////////////////////////////////////

        // only these 19 values in every 256 need testing.
        test((2187*(i + 27) + 2903) >> 8);
        test((729*(i + 31) + 697) >> 8);
        test((729*(i + 47) + 809) >> 8);
        test((729*(i + 63) + 665) >> 8);
        test((729*(i + 71) + 977) >> 8);
        test((729*(i + 91) + 989) >> 8);
        test((2187*(i + 103) + 2579) >> 8);
        test((729*(i + 111) + 745) >> 8);
        test((2187*(i + 127) + 2059) >> 8);
        test((729*(i + 155) + 925) >> 8);
        test((2187*(i + 159) + 2219) >> 8);
        test((729*(i + 167) + 881) >> 8);
        test((2187*(i + 191) + 2123) >> 8);
        test((729*(i + 207) + 905) >> 8);
        test((729*(i + 223) + 761) >> 8);
        test((729*(i + 231) + 817) >> 8);
        test((2187*(i + 239) + 2363) >> 8);
        test((729*(i + 251) + 1085) >> 8);
        test((6561*(i + 255) + 6305) >> 8);
    }

    return 0;
}

// use -fopt-info-vec for information on loop vectorisation.
// the `-march=native` means to compile for my specific CPU. Remove this flag for a more general exe
// gcc -O3 -fopenmp -flto -march=native main.c -o main.exe