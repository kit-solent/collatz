#include <stdio.h>
#include <omp.h>

int test(unsigned long long num) {
    unsigned long long init_num = num;
    while (num >= init_num) {
        if (num % 2 == 0) {
            num /= 2;
        } else {
            num = (3*num + 1)/2;
        }
    }
}

int main() {
    #pragma omp parallel for
    for (unsigned long long i = 3; i < 10000000000; i+=4) {
        test(i);
    }
    return 0;
}