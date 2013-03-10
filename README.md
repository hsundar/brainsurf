# brainsurf

Reconstruction of the brain surface from multiple images.

This project uses OpenCV primarily through its python interface. It shall be ported to C++ with a Qt based GUI later.

The repository tree should look like this,

brainsurf/
|_____ README.md
|
|_____ Python/
|         |______ calibrate.py
|         |______ pose_estimate.py
|         |______ reconstruct.py 
|
|_____ C++/
|_____ Data/
|         |______ calibration_target.pdf
|
|_____ Tests/

## Components

There are three main components to the project,

* Camera Calibration
* Pose Estimation
* 3D point cloud reconstruction

There will be separate command-line python scripts for each component. 

# calibrate

This script will take a set of images, along with parameters specifying the dimensions of the calibration target (checkerboard pattern) and estimate the intrinsic camera parameters. The script will also perform validation using back-projection and provide an estimate of the quality of the calibration

# pose_estimate

This script will take image(s) as input along with the intrinsic camera parameters and the dimensions of targets and estimate the pose(s) for each input. Ensure it is easy to call this from the reconstruct script

# reconstruct

This script will take a set (at least 2) of images along with their poses (obtained using *pose_estimate*) and the intrinsic camera parameters and estimate the brain surface in 3d. The output shall be a point cloud. Potentially, we can perform a Delaunay triangulation to generate the surface, followed by mesh smoothing.
  