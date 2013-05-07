import cv, sys, os
def cheese(no):
    print('testingcheese'+str(no))
def main():
    
    
    imgpath = '/home/michaelm/Documents/ecog/grids.jpg'
    img = cv.LoadImageM(imgpath)
    cv.NamedWindow('Test', flags=cv.CV_WINDOW_AUTOSIZE)
    
    #cv.CreateTrackbar('Threshold', 'Test', 50, 255, CallableFunction?)
    
    
    cv.ShowImage('Test', img)
    cv.WaitKey(0)
    print('DONE')
    
    # cv.SetTrackbarPos('trackbarName', 'windowName', int(pos)) #?
    # cv.WaitKey()
    
main()