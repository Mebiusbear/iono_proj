cmake_minimum_required(VERSION 3.1)

project(iono_proj)
set(CMAKE_CXX_FLAGS_RELEASE "-O3")
add_subdirectory(pybind11)

set(LIBRARY_OUTPUT_PATH ../src/apps/)

set (SRC_LIST 
        legendre)

foreach(SL ${SRC_LIST})
    pybind11_add_module(${SL} ${SL}.cpp)
endforeach()
