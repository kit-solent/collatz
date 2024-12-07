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
        // see simple.py for the algorithm behind these results
        /////////////////////////////////////////////////////////////
        // #form        | #result        | #transformation         //
        // 256n + 27    | 2187n + 242    | (2187/256)n + 6817/512  //
        // 256n + 31    | 729n + 91      | (729/256)n + 2315/512   //
        // 256n + 47    | 729n + 137     | (729/256)n + 2443/512   //
        // 256n + 63    | 729n + 182     | (729/256)n + 2251/512   //
        // 256n + 71    | 729n + 206     | (729/256)n + 2443/512   //
        // 256n + 91    | 729n + 263     | (729/256)n + 2443/512   //
        // 256n + 103   | 2187n + 890    | (2187/256)n + 6817/512  //
        // 256n + 111   | 729n + 319     | (729/256)n + 2315/512   //
        // 256n + 127   | 2187n + 1093   | (2187/256)n + 6689/512  //
        // 256n + 155   | 729n + 445     | (729/256)n + 2315/512   //
        // 256n + 159   | 2187n + 1367   | (2187/256)n + 6817/512  //
        // 256n + 167   | 729n + 479     | (729/256)n + 2443/512   //
        // 256n + 191   | 2187n + 1640   | (2187/256)n + 6817/512  //
        // 256n + 207   | 729n + 593     | (729/256)n + 2443/512   //
        // 256n + 223   | 729n + 638     | (729/256)n + 2443/512   //
        // 256n + 231   | 729n + 661     | (729/256)n + 2315/512   //
        // 256n + 239   | 2187n + 2051   | (2187/256)n + 6817/512  //
        // 256n + 251   | 729n + 719     | (729/256)n + 2443/512   //
        // 256n + 255   | 6561n + 6560   | (6561/256)n + 19939/512 //
        /////////////////////////////////////////////////////////////


        test(1287*(i + 27)/256 + );
    }

    return 0;
}

// the `-march=native` means to compile for my specific CPU. Remove this flag for a more general exe
// gcc -O3 -fopenmp -march=native main.c -o main.exe