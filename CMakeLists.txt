# cmake version to be used
cmake_minimum_required( VERSION 3.0 )

# project name
project(milano2)

# target
add_executable( milano2 milano2.cc )

# external libs
#find_package(Ceres REQUIRED)
# Or


#set(CERES_DIR "/home/move57924/installations/lib64/cmake/Ceres")

find_package(Ceres REQUIRED PATHS "/temp_local/mov57924/installations") #if the install directory is not in your PATH
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++17 -I/home/mov57924/Dokumente/Pythia6BNL/v1Code/include -L/home/mov57924/Dokumente/Pythia6BNL/v1Code/lib -laux")

#find_package(Ceres REQUIRED PATHS "/home/mov57924/installations") #if the install directory is not in your PATH
#set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++17 -I/home/mov57924/installations/include -L/home/mov57924/installations/lib -laux")

target_include_directories(milano2
  PRIVATE
    ${CERES_INCLUDE_DIRS}
)

target_link_libraries(milano2
  PRIVATE
    ${CERES_LIBRARIES}
)
