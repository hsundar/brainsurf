# opencv 2.4.5
# Python 2.7
import sys, os
import cv2 as cv
import numpy as np

# WaitKey == 27 not working properly
# What values for threshold in various algorithms

img = str(sys.argv[1]) #== to be updated later
mode = int(sys.argv[2])
image = cv.imread(img)
windowName = 'evalFeats.py'
trackbarName = 'Adjust'
curPos = 0 # Location of trackbar slider
endPos = 10000 #===

def main(image):
    #image = getImg()
    createGUI(windowName, trackbarName, curPos, endPos)
    #c = cv.waitKey() #need num?
    #while c != 27:
        #if c == 113: #n for next image
            #image = getImg()
        #if c == #p previous image
        #if c == #right arrow? Next alg
            #mode += 1
        #if c == #left arrow? Next alg
            #mode -= 1
        #showimg(image, mode)
    while cv.waitKey(15) != 27: #ESC
        showimg(image, mode)

def createGUI(windowName, trackbarName, curPos, endPos):
    cv.namedWindow(windowName, cv.CV_WINDOW_AUTOSIZE)
    cv.createTrackbar(trackbarName, windowName, curPos, endPos, barPos) # barPos(x) called when slider moved

def showimg(image, mode):
    curPos = cv.getTrackbarPos(trackbarName, windowName)
    imCopy = image.copy() # Create copy of image to draw pts on
    
    alg = getalg(curPos, mode)
    pts = alg.detect(imCopy)
    cv.drawKeypoints(imCopy, pts, imCopy, (0,255,0))
    cv.imshow(windowName, imCopy)
      
def barPos(x): # Updates curPos when trackbar slider moves
    curPos = x
    
def getalg(curPos, mode):
    if mode == 0:
        return cv.SURF(curPos, nOctaves=4, nOctaveLayers=2, extended=True, upright=False)
    elif mode == 1:
        return cv.SIFT()
    elif mode == 2:
        return cv.MSER()
    elif mode == 3:
        return cv.StarDetector()
    
main(image)    
