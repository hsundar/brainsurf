# opencv 2.4.5
# Python 2.7
import sys, os
import cv2 as cv
import numpy as np

# WaitKey not working properly
# What values for threshold in various algorithms
# Waitkeytime?

def main():
    dir = os.getcwd()
    print('Current directory: '+str(dir))
    mode = int(sys.argv[2])
    imgNo = 2
    image = getImg(dir, imgNo)
    
    windowName = 'evalFeats.py'
    trackbarName = 'Adjust'
    
    curPos = 0 # Location of trackbar slider
    endPos = 10000 #===
    createGUI(windowName, trackbarName, curPos, endPos)
    
    while cv.waitKey(5) != 27:
        if cv.waitKey(5) == 110: #n for next image
            print('next image')
            image = getImg(dir, imgNo)
        if cv.waitKey(5) == 112: #p previous image
            print('prev image')
        if cv.waitKey(5) == 62: #right arrow
            print('right arrow')
            mode += 1
            #if mode > _:
                #mode = 0
        if cv.waitKey(5) == 60:#left arrow
            print('left arrow')
            mode -= 1
            #if mode < _:
                #mode = _
        showimg(image, mode, trackbarName, windowName)
#     while cv.waitKey(15) != 27: #ESC
#         showimg(image, mode)
def getImg(dir, n):
    imagelist = [f for f in os.listdir(dir)]
    
    image = cv.imread(imagelist[n])
    return image
    
def createGUI(windowName, trackbarName, curPos, endPos):
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