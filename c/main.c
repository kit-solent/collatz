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
    const unsigned long long limit = 1000000000000;

    #pragma omp parallel for schedule(dynamic, 1024)
    for (unsigned long long i = 0; i < limit; i+=256) {
        // 0 means halving, 1 means 3n + 1 then halve.
        ////////////////////////////////////////////////////////////////////////////////////////////
        // 27       2187 ,  242      8,   [1, 1, 0, 1, 1, 1, 1, 1]    1     (2187/256, 2903/256)  //
        // 31       729  ,  91       8,   [1, 1, 1, 1, 1, 0, 1, 0]    2     (729/256, 697/256)    //
        // 47       729  ,  137      8,   [1, 1, 1, 1, 0, 1, 0, 1]    2     (729/256, 809/256)    //
        // 63       729  ,  182      8,   [1, 1, 1, 1, 1, 1, 0, 0]    2     (729/256, 665/256)    //
        // 71       729  ,  206      8,   [1, 1, 1, 0, 1, 0, 1, 1]    2     (729/256, 977/256)    //
        // 91       729  ,  263      8,   [1, 1, 0, 1, 1, 1, 0, 1]    2     (729/256, 989/256)    //
        // 103      2187 ,  890      8,   [1, 1, 1, 0, 1, 1, 1, 1]    1     (2187/256, 2579/256)  //
        // 111      729  ,  319      8,   [1, 1, 1, 1, 0, 1, 1, 0]    2     (729/256, 745/256)    //
        // 127      2187 ,  1093     8,   [1, 1, 1, 1, 1, 1, 1, 0]    1     (2187/256, 2059/256)  //
        // 155      729  ,  445      8,   [1, 1, 0, 1, 1, 1, 1, 0]    2     (729/256, 925/256)    //
        // 159      2187 ,  1367     8,   [1, 1, 1, 1, 1, 0, 1, 1]    1     (2187/256, 2219/256)  //
        // 167      729  ,  479      8,   [1, 1, 1, 0, 1, 1, 0, 1]    2     (729/256, 881/256)    //
        // 191      2187 ,  1640     8,   [1, 1, 1, 1, 1, 1, 0, 1]    1     (2187/256, 2123/256)  //
        // 207      729  ,  593      8,   [1, 1, 1, 1, 0, 0, 1, 1]    2     (729/256, 905/256)    //
        // 223      729  ,  638      8,   [1, 1, 1, 1, 1, 0, 0, 1]    2     (729/256, 761/256)    //
        // 231      729  ,  661      8,   [1, 1, 1, 0, 1, 1, 1, 0]    2     (729/256, 817/256)    //
        // 239      2187 ,  2051     8,   [1, 1, 1, 1, 0, 1, 1, 1]    1     (2187/256, 2363/256)  //
        // 251      729  ,  719      8,   [1, 1, 0, 1, 1, 0, 1, 1]    2     (729/256, 1085/256)   //
        // 255      6561 ,  6560     8,   [1, 1, 1, 1, 1, 1, 1, 1]    0     (6561/256, 6305/256)  //
        ////////////////////////////////////////////////////////////////////////////////////////////


        // i >> 1;  // i/2
        // i >> 2;  // i/4 (halving twice)
        // i >> 8;  // i/256

        // (2187/256)*(i + 27) + 2903/256
        // (2187*(i + 27) + 2903) >> 8
        // (2187*i + 61952) >> 8

        test((2187*(i + 27) + 61952) >> 8);
    }

    return 0;
}

// the `-march=native` means to compile for my specific CPU. Remove this flag for a more general exe
// gcc -O3 -fopenmp -march=native main.c -o main.exe