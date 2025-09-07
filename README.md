# Kruskal's algorithm for minimum spanning trees

## Introduction

This package consists of
 - an implementation of the union-find data structure (`UnionFind.h` and `UnionFind.cc`),
 - a data structure to represent edge-weighted graphs (`WeightedGraph.h` and `WeightedGraph.cc`),
 - an **incomplete** implementation of Kruskal's algorithm (`Kruskal.h` and `Kruskal.cc`),
 - a demo client that uses Kruskal's algorithm to construct an MST (`Exercise.cc`), and
 - unit tests for the `UnionFind`, `WeightedGraph` and the `Kruskal` classes (in the `tests` directory).

Your task is to complete the implementation of Kruskal's algorithm by extending the `src/Kruskal.cc` file with suitable lines of code. All building blocks that you need to do so are part of this package.

## Setup instructions
To build the given source code, you need a **C++ compiler** with support for C++11 features. Feel free to choose the build process that you are most comfortable with.

The recommended build process, however, is based on CMake. To execute it, you will need a working installation of **CMake** (version 3.10 or higher) and an appropriate build automation tool (such as GNU Make or Ninja). If you want to build and run the unit tests in the `tests` directory, **Google Test** needs to be installed on your machine as well. With all these requirements in place, perform the following steps:

 1. Navigate to the directory that contains the `CMakeLists.txt` file.
 2. Create and navigate into a `build` folder by executing `mkdir build` and `cd build`.
 3. Configure and generate by running the `cmake ..` command. If you have Google Test installed and want to build the unit tests, run `cmake -DBUILD_TESTS=ON ..` instead.
 4. Build all executables by running the `cmake --build .` command.

Doing so will create a `main` executable (`main.exe` if you are under Windows). This is the demo client mentioned above. Run it and you will see that its output is incorrect:
```
$ ./main
The minimum spanning tree (MST) of the given graph has
a total weight of 0 and consists of the following edges:
```

If you chose to build the unit tests, you can execute them by running the `gtest` (or `gtest.exe`) executable. Obviously, some `Kruskal`-related unit tests will fail:
```
[  FAILED  ] 3 tests, listed below:
[  FAILED  ] KruskalTest.PositiveWeights
[  FAILED  ] KruskalTest.NegativeWeights
[  FAILED  ] KruskalTest.NotConnected
```

## Your assignment
Complete the `src/Kruskal.cc` file. The public interface of the `Kruskal`, `UnionFind` and `WeightedGraph` classes are documented in the corresponding header files. Remember to rebuild the executables after making changes a source file. You can do so by executing `cmake --build .` if you went for CMake-based build.

A correct implementation should lead to the following output of `main`:
```
$ ./main
The minimum spanning tree (MST) of the given graph has
a total weight of 14 and consists of the following edges:
 1. v1 - v3
 2. v4 - v5
 3. v1 - v2
 4. v4 - v6
 5. v3 - v5
```
