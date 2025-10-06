cmake_minimum_required(VERSION 3.29)
project(SYSC4001_A1)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -static-libstdc++ -static-libgcc")

add_executable(SYSC4001_A1 interrupts.cpp)
