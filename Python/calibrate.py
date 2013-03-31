import cv, sys, time
# Variables
#src_img = sys.argv[]
#n_row = int( sys.argv[] )
#n_col = int( sys.argv[] )
    
# Temp. variables
src_img = '/home/wtrdrnkr/Documents/brainsurf/Data/calibration_target.jpg' # Input image of chessboard
dst_img = '/home/wtrdrnkr/Documents/brainsurf/Data/drawCorners.jpg' # Location to render image of found corners
n_row = 8
n_col = 6
patternSize = ( n_row, n_col )

def main():
    '''Determines intrinsic and extrinsic parameters of camera based on images \
    passed to calibrate.py'''
    corners()
    
def corners():
    '''Finds corners and renders them in dst_img'''
    # Load/convert image
    sys.stdout.write('Loading image as grayscale......')
    img_in = cv.LoadImageM( src_img, iscolor=0 ); print('DONE')
    
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
    img_out = cv.CreateMat(1100, 850, 0)
    cv.DrawChessboardCorners( img_out, patternSize, corners, retval ); print('DONE')
    
    # Save rendered corners
    sys.stdout.write('Saving file......')
    cv.SaveImage(dst_img, img_out); print('DONE'); print('    Location: %s')%dst_img

main()


#InitIntrinsicParams2D(objectPoints, imagePoints, npoints, imageSize, cameraMatrix, aspectRatio=1.)
#CalibrateCamera2(objectPoints, imagePoints, pointCounts, imageSize, cameraMatrix, distCoeffs, rvecs, tvecs, flags=0)
