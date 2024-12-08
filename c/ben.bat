@echo off
rem Regenerate executables and run the benchmarks.

rem Delete the two executables
if exist main.exe del main.exe
if exist benchmark.exe del benchmark.exe

rem Regenerate them
gcc -O3 -fopenmp -flto -march=native main.c -o main.exe
if errorlevel 1 (
    echo Failed to compile main.c
    exit /b 1
)

gcc -O3 -fopenmp -flto -march=native benchmark.c -o benchmark.exe
if errorlevel 1 (
    echo Failed to compile benchmark.c
    exit /b 1
)

rem Execute the benchmark file
benchmark.exe
if errorlevel 1 (
    echo Benchmark execution failed
    exit /b 1
)
