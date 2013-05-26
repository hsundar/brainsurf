cmake_minimum_required(VERSION 2.8)

project( brainsurf )

find_package( OpenCV REQUIRED )


## All executables are added here 

add_executable( camera_calibration camera_calibration.cpp )
target_link_libraries( camera_calibration ${OpenCV_LIBS} )

add_executable( mouse_coor_capture mouse_coor_capture.cpp )
target_link_libraries( mouse_coor_capture ${OpenCV_LIBS} )
