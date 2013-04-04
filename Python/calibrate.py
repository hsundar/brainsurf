# calibrate.py determines intrinsic/extrinsic attributes of a camera from input images
#
# Usage: python calibrate.py n_row n_col path_to_imgs
#
# Last modified: 4/3/2013
#
# Currently working on:
#    - convert to 8bit
#    - calibrate() function
#    - Auto recognize dimensions of input imgs
#    - Auto recognize patternSize

import cv, sys, os
if len(sys.argv) > 1: #if called from command line
    n_row = int( sys.argv[1] )
    n_col = int( sys.argv[2] )
    path_to_imgs = str( sys.argv[3] )
else: # Temp. variables (for development)
    path_to_imgs = '/home/wtrdrnkr/Pictures/Calib_images/' # Retrieves from and saves to
    n_row = 9
    n_col = 6

# Global Variables
dims = (3744, 2104) # Dimensions of input img
n_pts = dims[0]*dims[1] #=== number of points=pixels?
patternSize = ( n_row, n_col )

def main():
    '''Determines intrinsic and extrinsic parameters of camera by use of images \
    in the path passed to calibrate.py'''
    cornerList = []
    # Add corners from each img into ptList
    # Each set of corners is its own element
    for src_img in os.listdir(path_to_imgs):
        if 'crn' not in src_img: # prevents corner()ing of rendered corners
            cornerList.append(getcorners(src_img))
    print(cornerList)
    #calibrate(c)
    
def getcorners(src_img):
    '''Finds corners and renders them in dst_img'''
    # Load/convert image
    print('Loading %s as grayscale......')%src_img,
    path = path_to_imgs+src_img
    img_in = cv.LoadImageM( path, iscolor=0 ); print('DONE')
    
    # Find corners
    print('Finding corners......'),
    retval, corners = cv.FindChessboardCorners( img_in, patternSize )
    if retval != 1:print('CORNERS NOT FOUND'); print('END'); quit()
    else:
        # Refine corners: !!!!check parameters!!!! ===
        corners = cv.FindCornerSubPix(img_in, corners, (5,5), (-1,-1), (cv.CV_TERMCRIT_EPS,0,.01)); print('DONE')

    # Render corners in matrix
    print('Rendering found corners......'),
    img_out = cv.CreateMat(dims[1], dims[0], 0)
    cv.DrawChessboardCorners( img_out, patternSize, corners, retval ); print('DONE')
    
#     # Show preview image of rendered corners
#     cv.ShowImage('Out', img_out)
#     cv.WaitKey(2500)
    
    # Save rendered corners
    print('Saving file......'),
    dst_img = path_to_imgs+'crn'+src_img
    cv.SaveImage(dst_img, img_out); print('DONE'); print('    Location: %s\n')%dst_img

    return corners

def calibrate(corners):
    # === NOT WORKING YET
    opts = cv.CreateMat(n_img * n_pts, 3, cv.CV_32FC1)
    ipts = cv.CreateMat(corners* n_pts, 2, cv.CV_32FC1)
    npts = cv.CreateMat(n_img, 1, cv.CV_32SC1)
    
    
    
    
main()


#InitIntrinsicParams2D(objectPoints, imagePoints, npoints, imageSize, cameraMatrix, aspectRatio=1.)
#CalibrateCamera2(objectPoints, imagePoints, pointCounts, imageSize, cameraMatrix, distCoeffs, rvecs, tvecs, flags=0)
