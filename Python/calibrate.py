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
    image_in = cv.LoadImage( src_img, iscolor=0 ); print('DONE') # matrix

    # Find corners
    sys.stdout.write('Finding corners......')
    retval, corners = cv.FindChessboardCorners( image_in, patternSize )
    if retval != 1:
        print('CORNERS NOT FOUND')
        print('END')
        quit()
    else:
        print('DONE');

    # Render corners
    sys.stdout.write('Rendering found corners......'),
    image_out = cv.CreateMat(1100, 850, 0) # Height/width of image (px)
    cv.DrawChessboardCorners( image_out, patternSize, corners, retval ); print('DONE')
    
    sys.stdout.write('Saving file......'),
    cv.SaveImage(dst_img, image_out); print('DONE'); print('    Location: %s')%dst_img

main()


#InitIntrinsicParams2D(objectPoints, imagePoints, npoints, imageSize, cameraMatrix, aspectRatio=1.)
#CalibrateCamera2(objectPoints, imagePoints, pointCounts, imageSize, cameraMatrix, distCoeffs, rvecs, tvecs, flags=0)
