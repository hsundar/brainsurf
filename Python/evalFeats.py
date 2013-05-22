# opencv 2.4.5
# Python 2.7
import sys, os
import cv2 as cv
import numpy as np
import imghdr

# WaitKey works with qt, requires holding down sometimes
# What values for threshold in various algorithms
# Qt button options (not in python?): http://docs.opencv.org/modules/highgui/doc/qt_new_functions.html#
# Multiple trackbars?
'''Brainsurf feature evaluator.
In commandline, call from folder containing the images:
    python <path_to>evalFeats.py <mode>
    
Modes:
    0 - SURF
    1 - SIFT
    2 - MSER
    3 - StarDetector
'''
def main():
    dir = os.getcwd()
    print('Current directory: '+str(dir))
    mode = int(sys.argv[1])
    imgNo = 0
    image = getImg(dir, imgNo)
    
    windowName = 'evalFeats.py'
    trackbarName = 'Adjust'
    
    curPos = 0 # Location of trackbar slider
    endPos = 10000 #===
    createGUI(windowName, trackbarName, curPos, endPos)

    while cv.waitKey(5) != 113: # 'q' for quit
        if cv.waitKey(5) == 110: # 'n' for next image
            print('NEXT IMAGE')
            imgNo += 1
            image = getImg(dir, imgNo)
        if cv.waitKey(5) == 112: # 'p' previous image
            print('PREVIOUS IMAGE')
            imgNo -= 1
            image = getImg(dir, imgNo)
        if cv.waitKey(5) == 62: # '>' for mode + 1
            print('MODE + 1')
            mode += 1
            if mode > 3:
                mode = 0
        if cv.waitKey(5) == 60: # '<' for mode - 1
            print('MODE - 1')
            mode -= 1
            if mode < 0:
                mode = 3
        showimg(image, mode, trackbarName, windowName)
    print ('QUIT')

def getImg(dir, n):
    imagelist = [f for f in os.listdir(dir) if imghdr.what(f) != None] #imghdr returns None if not an img type
    if n >= len(imagelist):
        n = 0
    elif n < 0:
        n = len(imagelist)-1
    image = cv.imread(imagelist[n])
    print('Current image: '+str(imagelist[n]))
    return image
    
def createGUI(windowName, trackbarName, curPos, endPos):
    # Different GUI for each feature detector?
    cv.namedWindow(windowName, cv.CV_WINDOW_AUTOSIZE)
    cv.createTrackbar(trackbarName, windowName, curPos, endPos, barPos) # barPos(x) called when slider moved

def showimg(image, mode, trackbarName, windowName):
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
        return cv.SIFT(curPos)
    elif mode == 2:
        return cv.MSER(curPos)
    elif mode == 3:
        return cv.StarDetector(curPos)
    
main()