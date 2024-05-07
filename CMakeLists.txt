cmake_minimum_required(VERSION 3.18...3.29)
project(${SKBUILD_PROJECT_NAME} LANGUAGES C)

set(LIBDEFLATE_BUILD_SHARED_LIB OFF)
add_subdirectory(libdeflate EXCLUDE_FROM_ALL)

find_package(Python REQUIRED COMPONENTS Development)

python_add_library(deflate MODULE deflate.c)
target_link_libraries(deflate PRIVATE libdeflate_static)
install(TARGETS deflate LIBRARY DESTINATION .)
