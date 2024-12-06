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
    const unsigned long long limit = 100000000000;

    #pragma omp parallel for schedule(dynamic, 1024)
    for (unsigned long long i = 0; i < limit; i+=256) {
        // 0 means halving, 1 means 3n + 1 then halve.
        //////////////////////////////////////////////////////////////////
        // 27       2187 ,  242      8,   [1, 1, 0, 1, 1, 1, 1, 1]    1 //
        // 31       729  ,  91       8,   [1, 1, 1, 1, 1, 0, 1, 0]    2 //
        // 47       729  ,  137      8,   [1, 1, 1, 1, 0, 1, 0, 1]    2 //
        // 63       729  ,  182      8,   [1, 1, 1, 1, 1, 1, 0, 0]    2 //
        // 71       729  ,  206      8,   [1, 1, 1, 0, 1, 0, 1, 1]    2 //
        // 91       729  ,  263      8,   [1, 1, 0, 1, 1, 1, 0, 1]    2 //
        // 103      2187 ,  890      8,   [1, 1, 1, 0, 1, 1, 1, 1]    1 //
        // 111      729  ,  319      8,   [1, 1, 1, 1, 0, 1, 1, 0]    2 //
        // 127      2187 ,  1093     8,   [1, 1, 1, 1, 1, 1, 1, 0]    1 //
        // 155      729  ,  445      8,   [1, 1, 0, 1, 1, 1, 1, 0]    2 //
        // 159      2187 ,  1367     8,   [1, 1, 1, 1, 1, 0, 1, 1]    1 //
        // 167      729  ,  479      8,   [1, 1, 1, 0, 1, 1, 0, 1]    2 //
        // 191      2187 ,  1640     8,   [1, 1, 1, 1, 1, 1, 0, 1]    1 //
        // 207      729  ,  593      8,   [1, 1, 1, 1, 0, 0, 1, 1]    2 //
        // 223      729  ,  638      8,   [1, 1, 1, 1, 1, 0, 0, 1]    2 //
        // 231      729  ,  661      8,   [1, 1, 1, 0, 1, 1, 1, 0]    2 //
        // 239      2187 ,  2051     8,   [1, 1, 1, 1, 0, 1, 1, 1]    1 //
        // 251      729  ,  719      8,   [1, 1, 0, 1, 1, 0, 1, 1]    2 //
        // 255      6561 ,  6560     8,   [1, 1, 1, 1, 1, 1, 1, 1]    0 //
        //////////////////////////////////////////////////////////////////

        // i >> 1;  // i/2
        // i >> 2;  // i/4 (halving twice)

        test(i + 27);
    }

    return 0;
}

// the -march=native means to compile for my specific CPU. Remove this flag for a more general exe
// gcc -O3 -fopenmp -march=native main.c -o main.exe