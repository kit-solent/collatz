import pathlib, subprocess, time, os

def generate_unique_name(base:str = "file"):
    counter = 0
    while os.path.exists(base+hex(counter)[2:]):
        counter += 1
    return base+hex(counter)[2:]


def benchmark(file:pathlib.Path, compile_flags:list, runs:int=10):
    """
    Compiles, runs, and returns the excecution time of the given C file.
    Compilation is done using gcc with the provided flags.
    The file is run `runs` times and the results are averaged.
    """
    # generate a unique name for the excecutable to ensure
    excecutable = generate_unique_name("excecutable")

    # compile the given C file.
    try:
        subprocess.run(["gcc", *compile_flags, file, "-o", excecutable])
    except subprocess.CalledProcessError as err:
        print(f"Failed to compile: {file}.")
        return err

    # benchmark the file
    times = []
    for i in range(runs):
        try:
            start_time = time.perf_counter()
            code = subprocess.run([f"./{excecutable}"]).returncode
            end_time = time.perf_counter()
        except subprocess.CalledProcessError as err:
            print(f"File: {file} failed to excecute with error: {err} on run: {i + 1}")

            # delete the generated excecutable
            os.remove(excecutable)

            return err

        times.append(end_time - start_time)

    # delete the generated excecutable
    os.remove(excecutable)

    # average and return the results
    return sum(times)/len(times), code


if __name__ == "__main__":
    # gcc -O3 -fopenmp -m64 -funroll-loops -march=native main.c -o main
    # exclude -march=native as we want our benchmarks to be for a more general executable.
    flags = ["-O3", "-fopenmp", "-m64", "-funroll-loops"]

    print("Benchmarking file: main.c")
    result1 = benchmark("main.c", flags)
    print("\n")
    print("Benchmarking file: main2.c")
    result2 = benchmark("main2.c", flags)
    if len(result1) == 2:
        print("\n")
        print(f"Excecution time for main.c: {round(result1[0],3)}s")
        print(f"Return code for main.c: {result1[1]}")
    if len(result2) == 2:
        print()
        print(f"Excecution time for main2.c: {round(result2[0],3)}s")
        print(f"Return code for main2.c: {result2[1]}")
    if len(result1) + len(result2) == 4:
        print()
        print(("main2.c" if result1[0] > result2[0] else "main.c") + f" was faster by: {round(abs(result1[0] - result2[0]),3)}s")