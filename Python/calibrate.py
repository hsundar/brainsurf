'''This script will take a set of images, along with parameters \
specifying the dimensions of the calibration target (checkerboard \
pattern) and estimate the intrinsic camera parameters. The script \
will also perform validation using back-projection and provide an \
estimate of the quality of the calibration. \n \n \
Should be called in command line as: \n python \
<path_to_calibrate.py> <list_of_images> <points_per_row> \
<points_per_col>'''

import cv
import sys

image = cv.LoadImage('/home/michaelm/Documents/brainsurf/IMG_0364.jpg') #!!
pts_in_row = 9 #!!
pts_in_column = 6 #!!
patternSize = (pts_in_row, pts_in_column)

# Find corners
retval, corners = cv.FindChessboardCorners(image, patternSize)


#========================== vv Being Developed vv ===========================
# Draw corners
cv.DrawChessboardCorners(image, patternSize, corners, retval)











#===================== vv For command line functionality vv ====================
### sys.argv is a list of the command-line arguments
##    
### Build list of images to be processed
##imgList = open( str(sys.argv[1]),'r' ) # file object for the imageList
##images = buildImageList( imageList ) # list of images as strings
##imgList.close()
##
###get patternSize
##points_per_row = sys.argv[2]
##points_per_col = sys.argv[3]
##patternSize = cv.cvSize(points_per_row, points_per_column)
##
##
####    retval, corners = cv.findChessboardCorners(image, patternSize)
##
##def buildImageList( imageList ):
##    '''Returns a list strings that are the paths to the images to be processed.'''
##    images = []
##
##    for line in imageList:
##        images.append( str(line) )
##
##    return images
        
