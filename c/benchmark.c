#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
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

    // Print the time taken
    printf("Execution time: %.6f seconds\n", time_taken);
    printf("Result: %d\n", result);

    return 0;
}
