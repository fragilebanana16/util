cmake_minimum_required(VERSION 2.8)

option (DEBUG_ON "debug the program" ON)
if (DEBUG_ON)
    SET(CMAKE_BUILD_TYPE "Debug")
    SET(CMAKE_CXX_FLAGS_DEBUG "$ENV{CXXFLAGS} -O0 -Wall -g2 -ggdb")
    SET(CMAKE_CXX_FLAGS_RELEASE "$ENV{CXXFLAGS} -O3 -Wall")
endif (DEBUG_ON)

project( TW )
find_package( OpenCV REQUIRED )
add_definitions(-std=c++11)
include_directories( ${OpenCV_INCLUDE_DIRS} )
add_executable( cvtest cvtest.cpp )
target_link_libraries( cvtest ${OpenCV_LIBS})

