# Currently working on:
#    - Multiple images


import cv, sys, os
# Variables
#src_img = sys.argv[]
#n_row = int( sys.argv[] )
#n_col = int( sys.argv[] )
    
# Temp. variables
path_to_images = '/home/wtrdrnkr/Pictures/Calib_images/'
#src_img = '/home/wtrdrnkr/Documents/brainsurf/Data/calibration_target.jpg' # Input image of chessboard
dims = (850, 1100)
n_pts = dims[0]*dims[1] #=== number of points?
#dst_img = '/home/wtrdrnkr/Documents/brainsurf/Data/drawCorners.jpg' # Location to render image of found corners
n_row = 8
n_col = 6
patternSize = ( n_row, n_col )

def main():
    '''Determines intrinsic and extrinsic parameters of camera based on images \
    passed to calibrate.py'''
    ptList = []
    count = 0
    for src_img in os.listdir(path_to_images):
        ptList.append(corners(src_img))
    print(ptList)
    #calibrate(c)
    
def corners(src_img):
    '''Finds corners and renders them in dst_img'''
    # Load/convert image
    sys.stdout.write('Loading %s as grayscale......')%str(src_img)
    img_in = cv.LoadImageM( path_to_images+src_img, iscolor=0 ); print('DONE')
    
    # Find corners
    sys.stdout.write('Finding corners......')
    retval, corners = cv.FindChessboardCorners( img_in, patternSize )
    if retval != 1:
        print('CORNERS NOT FOUND');print('END');quit()
    else:
        # Refine corners: !!!!check parameters!!!! ===
        corners = cv.FindCornerSubPix(img_in, corners, (5,5), (-1,-1), (cv.CV_TERMCRIT_EPS,0,.01)); print('DONE')

    # Render corners in matrix
    sys.stdout.write('Rendering found corners......')
    img_out = cv.CreateMat(dims[1], dims[0], 0)
    cv.DrawChessboardCorners( img_out, patternSize, corners, retval ); print('DONE')
    
    # Show preview image of rendered corners
    cv.ShowImage('Out', img_out)
    cv.WaitKey(2500)
    
    # Save rendered corners
    sys.stdout.write('Saving file......')
    cv.SaveImage(dst_img, img_out); print('DONE'); print('    Location: %s')%dst_img

    return corners

def calibrate(corners):
    # === NOT WORKING YET
    opts = cv.CreateMat(n_img * n_pts, 3, cv.CV_32FC1)
    ipts = cv.CreateMat(corners* n_pts, 2, cv.CV_32FC1)
    npts = cv.CreateMat(n_img, 1, cv.CV_32SC1)
    
    
    
    
main()


#InitIntrinsicParams2D(objectPoints, imagePoints, npoints, imageSize, cameraMatrix, aspectRatio=1.)
#CalibrateCamera2(objectPoints, imagePoints, pointCounts, imageSize, cameraMatrix, distCoeffs, rvecs, tvecs, flags=0)
