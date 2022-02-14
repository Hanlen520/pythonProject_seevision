cmake_minimum_required(VERSION 3.5)

set(CONTROLL_DEMO test)

project(${CONTROLL_DEMO} LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
file(GLOB TEST_SOURCE
    ${CMAKE_CURRENT_SOURCE_DIR}/*.h
    ${CMAKE_CURRENT_SOURCE_DIR}/*.hpp
    ${CMAKE_CURRENT_SOURCE_DIR}/*.c
    ${CMAKE_CURRENT_SOURCE_DIR}/*.cpp
    )

link_directories(lib)

add_executable(${CONTROLL_DEMO} ${TEST_SOURCE})


target_link_libraries(${CONTROLL_DEMO} pthread svctrl_factory)

target_include_directories(${CONTROLL_DEMO} PRIVATE ${CMAKE_SOURCE_DIR}/include)
