cmake_minimum_required(VERSION 3.5)

project(GameOfLife LANGUAGES CXX)

option(MAKE_TEST "Making unit tests" OFF)
message("MAKE_TEST: ${MAKE_TEST}")

add_subdirectory(lib)
if (${MAKE_TEST})
	add_subdirectory(test)
else()
endif()
add_executable(game_of_life main.cpp)

target_link_libraries(game_of_life PRIVATE GameClasses)
target_link_libraries(game_of_life PRIVATE Interface)

