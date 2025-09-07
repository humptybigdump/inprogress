cmake_minimum_required(VERSION 3.10)
project(kruskal-example LANGUAGES CXX)

option(BUILD_TESTS "Build unit tests")

add_library(kruskal
    src/Kruskal.cc
    src/UnionFind.cc
    src/WeightedGraph.cc
)

add_executable(main
    src/Exercise.cc
)

target_include_directories(kruskal PUBLIC include)
target_compile_features(kruskal PUBLIC cxx_std_11)

target_link_libraries(main PRIVATE kruskal)

if (BUILD_TESTS)
    find_package(GTest REQUIRED)
    enable_testing()

    add_executable(gtest
        tests/KruskalTest.cc
        tests/UnionFindTest.cc
        tests/WeightedGraphTest.cc
    )

    target_include_directories(gtest PRIVATE include)
    target_link_libraries(gtest kruskal GTest::GTest GTest::Main)
    gtest_discover_tests(gtest)
endif()
