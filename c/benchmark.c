#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
    // main.c
    struct timespec start_time, end_time;

    // Record the start time
    clock_gettime(CLOCK_MONOTONIC, &start_time);

    // Your code here (e.g., calling a function or performing a task)
    int result = system("./main");

    // Record the end time
    clock_gettime(CLOCK_MONOTONIC, &end_time);

    // Calculate the time taken
    double time_taken = (end_time.tv_sec - start_time.tv_sec) +
                        (end_time.tv_nsec - start_time.tv_nsec) / 1000000000.0;


    // main2.c
    struct timespec start_time2, end_time2;

    // Record the start time
    clock_gettime(CLOCK_MONOTONIC, &start_time2);

    // Your code here (e.g., calling a function or performing a task)
    int result2 = system("./main2");

    // Record the end time
    clock_gettime(CLOCK_MONOTONIC, &end_time2);

    // Calculate the time taken
    double time_taken2 = (end_time2.tv_sec - start_time2.tv_sec) +
                        (end_time2.tv_nsec - start_time2.tv_nsec) / 1000000000.0;



    // Print the time taken
    printf("\n");
    printf("Execution time for main.c: %.6f seconds\n", time_taken);
    printf("Exit code for main.c: %d\n", result);
    printf("\n");
    printf("Execution time for main2.c: %.6f seconds\n", time_taken2);
    printf("Exit code for main2.c: %d\n", result2);

    return 0;
}
