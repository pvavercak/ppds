cmake_minimum_required(VERSION 3.0)

project(counter VERSION 0.0.1 LANGUAGES C CXX)

set(CMAKE_CXX_STANDARD 17)

add_executable(counter src/counter.cpp)

target_link_libraries(counter PRIVATE pthread)

enable_testing()

add_test(NAME test_counter COMMAND counter WORKDIR ${CMAKE_CURRENT_BINARY_DIR})