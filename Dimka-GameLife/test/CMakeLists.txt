cmake_minimum_required(VERSION 3.5)

project(test LANGUAGES CXX)

option(GET_GTESTS "Downlods gtests from URL." ON)
message("GET_GTESTS: ${GET_GTESTS}")

if (${GET_GTESTS})
	include(FetchContent)
		FetchContent_Declare(googletest
		URL https://github.com/google/googletest/archive/03597a01ee50ed33e9dfd640b249b4be3799d395.zip)

	set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
	FetchContent_MakeAvailable(googletest)
endif()

add_executable(test test.cpp)
if (${GET_GTESTS})
	target_link_libraries(test PRIVATE GTest::gtest_main)
else()
	target_link_libraries(test PRIVATE gtest pthread)
endif()

enable_testing()

target_link_libraries(test PUBLIC GameClasses)

include(GoogleTest)
gtest_discover_tests(test)

