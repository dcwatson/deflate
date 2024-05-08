cmake_minimum_required(VERSION 3.18...3.29)
project(${SKBUILD_PROJECT_NAME} LANGUAGES C)

find_package(Python REQUIRED COMPONENTS Interpreter Development.Module)

python_add_library(deflate_ext MODULE deflate.c)
set_property(TARGET deflate_ext PROPERTY OUTPUT_NAME deflate)

if(DEFINED ENV{LIBDEFLATE_PREFIX})
    message(STATUS "Finding libdeflate in $ENV{LIBDEFLATE_PREFIX}")
    target_include_directories(deflate_ext PUBLIC "$ENV{LIBDEFLATE_PREFIX}/include")
    target_link_directories(deflate_ext PUBLIC "$ENV{LIBDEFLATE_PREFIX}/lib")
    target_link_libraries(deflate_ext PRIVATE deflate)
else()
    message(STATUS "Building and linking bundled libdeflate")
    set(CMAKE_POSITION_INDEPENDENT_CODE ON)
    set(LIBDEFLATE_BUILD_SHARED_LIB OFF)
    add_subdirectory(libdeflate EXCLUDE_FROM_ALL)
    target_link_libraries(deflate_ext PRIVATE libdeflate_static)
endif()

install(TARGETS deflate_ext LIBRARY DESTINATION .)
