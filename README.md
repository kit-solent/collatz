# Collatz
A collection of algorithms relating to the Collatz Conjecture.
[https://en.wikipedia.org/wiki/Collatz_conjecture](https://en.wikipedia.org/wiki/Collatz_conjecture)

As shown in main/calculations.py, for every chunk of 256 numbers i.e. numbers of the form 256n + k where k ranges from 0 to 255, \
there are only 19 values that don't fall below their starting value and these values can be precomputed 14 or 15 steps.

c/main.c is a C program to computationally verify the conjecture using optimisations calculated and explained in main/calculations.py
The rest of the c directory contains benchmarking files.

main/main.py is the set of classes and functions (in Python) that are used by calculations.py to find patterns and optimisations for c/main.c.

main/template.c is a C file to facilitate generation of C programs for testing given ranges of numbers.


misc contains a bunch stuff I'm not using anymore. thingy.xlsx is an excel document for trying to find more patterns and visualise them.