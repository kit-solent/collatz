# Collatz
A collection of algorithms relating to the Collatz Conjecture.
[https://en.wikipedia.org/wiki/Collatz_conjecture](https://en.wikipedia.org/wiki/Collatz_conjecture)

c/main.c is a C program to computationally verify the conjecture using optimisations calculated and explained in main/calculations.py
The rest of the c directory contains benchmarking files.

main/main.py is the set of classes and functions (in Python) that are used by calculations.py to find patterns and optimisations for c/main.c
main/template.c is a C file to facilitate generation of C programs for testing given ranges of numbers.

misc contains a bunch stuff I'm not using anymore. thingy.xlsx is an excel document for trying to find more patterns and visualise them.