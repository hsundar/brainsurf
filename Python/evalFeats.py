# opencv 2.4.5
# Python 2.7
import sys, os
import cv2 as cv
import numpy as np
# cv.ExtractSURF()
# cv.GetStarKeypoints()
# cv.Canny(image, edges, threshold1, threshold2)
# cv.CornerHarris(image, harris_dst, blockSize)
# cv.CornerMinEigenVal(image, eigenval, blockSize)
# cv.CornerEigenValsAndVecs(image, eigenvv, blockSize)
# cv.FindCornerSubPix(image, corners, win, zero_zone, criteria)
# cv.GoodFeaturesToTrack(image, eigImage, tempImage, cornerCount, qualityLevel, minDistance)
# cv.HoughLines2(image, storage, method, rho, theta, threshold)
# cv.PreCornerDetect(image, corners)

# WaitKey == 27 not working properly
# What values for threshold in various algorithms

if len(sys.argv) > 1:
    print('Command Line')
    dir = os.getcwd()+'/'
    img = str(sys.argv[1]) #== to be updated later
    print('Current image: '+img)
#     if sys.argv[2] == 0:
#         alg = surf()
#     elif sys.argv[2] == 1:
#         alg = sift()

image = cv.imread(img)
windowName = 'evalFeats.py'
trackbarName = 'Adjust'
strtPos = 0 # Location of trackbar slider
endPos = 10000

def main():
    cv.namedWindow(windowName, cv.CV_WINDOW_AUTOSIZE)
    cv.createTrackbar(trackbarName, windowName, strtPos, endPos, barPos)
    while True:
        showimg(image)
        if cv.waitKey(15) == 27: #ESC
            print('END')
            break
        elif cv.waitKey(15) == 110: #'n' for next image
            nextimg = 'asdfasdf'
#             image = cv.imread(nextimg)
            print('NEXT IMAGE')
            
            
        
def showimg(image):
    strtPos = cv.getTrackbarPos(trackbarName, windowName)
    imCopy = image.copy() # Create copy of image to draw pts on
    surf = cv.SURF(strtPos, nOctaves=4, nOctaveLayers=2, extended=True, upright=False)
    pts = surf.detect(imCopy)
    cv.drawKeypoints(imCopy, pts, imCopy, (0,0,255))
    cv.imshow(windowName, imCopy)
    
def barPos(x): # Updates strtPos when trackbar slider moves
    strtPos = x
# def surf():
#     return windowName, trackbarName, strtPos, endPos
main()    
