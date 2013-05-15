# opencv 2.4.3
# Python 2.7
import cv2 as cv
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
# Previous pts not going away

img = '/home/michaelm/Documents/ecog/grids.jpg'
image = cv.imread(img)
windowName = 'evalFeats.py'
trackbarName = 'Adjust'
strtPos = 0
endPos = 255

# Circle properties
radius = 30
color = (0,0,255)
thickness = 2
connectivity = 8

def main():
    cv.namedWindow(windowName, cv.CV_WINDOW_AUTOSIZE)
    cv.createTrackbar(trackbarName, windowName, strtPos, endPos, barPos)
    while cv.waitKey(10) != 27:
        showimg(image)

def showimg(image):
    imCopy = image
    pts = [(x,y) for (x,y) in [(cv.getTrackbarPos(trackbarName, windowName), cv.getTrackbarPos(trackbarName, windowName))]]
    for pt in pts:
        cv.circle(imCopy, pt,radius,color,thickness,connectivity)
    cv.imshow(windowName, imCopy) 
      
def barPos(x):
    strtPos = x

main()    


# def main(image):
#     name = 'evalFeats'
#     # Point attributes
#     radius = 30
#     thickness = 2
#     connectivity = 8
#     green = cv.CV_RGB(0,250,0)
#     # Create window & trackbar
#     cv.NamedWindow(name, 1)
#     cv.CreateTrackbar('Threshold', name, cur_pos, 255, switch_callback)
#     # Show pts
#     while True:
#         # Detected points
#         testpt = (cv.GetTrackbarPos('Threshold', name),cv.GetTrackbarPos('Threshold', name))
#         pts = [testpt] #list of points returned from feature detection
#         for pt in pts:
#             cv.Circle(image,pt,radius,green,thickness,connectivity)
#         cv.ShowImage(name, image)
#         # Key to quit
#         if cv.WaitKey( 15 ) == 27: # ESC
#             break
#     cv.DestroyWindow( name )

def switch_callback( position ):
    cur_pos = position

#main(image)
def test(image):
    img = cv.LoadImageM('/home/michaelm/Documents/ecog/grids.jpg', cv.CV_LOAD_IMAGE_GRAYSCALE)
    eig_image = cv.CreateMat(img.rows, img.cols, cv.CV_32FC1)
    temp_image = cv.CreateMat(img.rows, img.cols, cv.CV_32FC1)
    
    # Point attributes
    radius = 30
    thickness = 2
    connectivity = 8
    green = cv.CV_RGB(0,250,0)
    
    
    alg = cv.GoodFeaturesToTrack(img, eig_image, temp_image, cur_pos, 0.04, 1.0, useHarris=True)
    pts = [(x,y) for (x,y) in alg]
    cv.NamedWindow('test')
    #cv.CreateTrackbar('Threshold', name, cur_pos, 255, switch_callback)  
    
    while True:
        for pt in pts:
            cv.Circle(img, (int(pt[0]),int(pt[1])), radius, green, thickness, connectivity )
        cv.ShowImage('test', img)
        if cv.WaitKey(15) == 27:
            break
    cv.DestroyWindow('test')    
#test(image)
