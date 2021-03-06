# opencv 2.4.5
# Python 2.7
import sys, os
import cv2 as cv
import numpy as np
import imghdr

# Algorithms dont return values in same format
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
    print('Press "q" to quit\n"n" for next image\n"p" for previous image\n"." for next algorithm\n"," for previous algorithm')
    mode = int(sys.argv[1])
    imgNo = 0
    image = getImg(dir, imgNo)
    
    windowName = 'evalFeats.py'
    trackbarName = 'Adjust'
    
    curPos = 0 # Location of trackbar slider
    endPos = 10000 #===
    createGUI(windowName, trackbarName, curPos, endPos)
    
    c = 0
    while c != 113: # 'q' for quit
        c = cv.waitKey(1)
        if c == 110: # 'n' for next image
            print('NEXT IMAGE')
            imgNo += 1
            image = getImg(dir, imgNo)
        elif c == 112: # 'p' previous image
            print('PREVIOUS IMAGE')
            imgNo -= 1
            image = getImg(dir, imgNo)
        elif c == 46: # '.' for mode + 1
            print('MODE + 1')
            mode += 1
            if mode > 3:
                mode = 0
        elif c == 44: # ',' for mode - 1
            print('MODE - 1')
            mode -= 1
            if mode < 0:
                mode = 3
        showimg(image, mode, trackbarName, windowName)
    print ('QUIT')

def getImg(dir, n):
    imagelist = [f for f in os.listdir(dir) if imghdr.what(f) != None] #imghdr returns None if not an image
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
    
    # Different cases for different algs
    if mode in [0,1]:
        pts = alg.detect(imCopy)
        cv.drawKeypoints(imCopy, pts, imCopy, (0,255,0))
    elif mode in [2]:
        pts = alg.detect(imCopy)
        print(pts)
    cv.imshow(windowName, imCopy)
      
def barPos(x): # Updates curPos when trackbar slider moves
    curPos = x

def getalg(curPos, mode):
    if mode == 0:
        return cv.SURF(curPos, nOctaves=4, nOctaveLayers=2, extended=True, upright=False)
    elif mode == 1:
        return cv.SIFT(curPos)
    elif mode == 2: #=== does not return keypts like other algs (features2d.hpp; convert function)
        return cv.MSER(curPos) # vector<vector<pt>>
    elif mode == 3: #=== does not return keypts like other algs...
        return cv.StarDetector(curPos)
    
main()