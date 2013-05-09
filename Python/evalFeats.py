import cv, sys, os
# Problems:
# == Cant find feature detection algorithms (python)
# == How to get rid of previous detected pts as trackbar moves

image = cv.LoadImageM('/home/michaelm/Documents/ecog/grids.jpg')
cur_pos = 0
def main(image):
    name = 'evalFeats'
    # Point attributes
    radius = 30
    thickness = 2
    connectivity = 8
    green = cv.CV_RGB(0,250,0)
    
    # Create window & trackbar
    cv.NamedWindow(name, 1)
    cv.CreateTrackbar('Threshold', name, cur_pos, 255, switch_callback)

    while True:
        # Detected points
        testpt = (cv.GetTrackbarPos('Threshold', name),cv.GetTrackbarPos('Threshold', name))
        pts = [testpt] #list of points returned from feature detection
        for pt in pts:
            cv.Circle(image,pt,radius,green,thickness,connectivity)
        
        cv.ShowImage(name, image)

        # Key to quit
        if cv.WaitKey( 15 ) == 27: # ESC
            break
    
    cv.DestroyWindow( name )

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
    
    pts = []
    alg = cv.GoodFeaturesToTrack(img, eig_image, temp_image, cur_pos, 0.04, 1.0, useHarris=True)
    for (x,y) in alg:
        pts.append((x,y))
    cv.NamedWindow('test')
    cv.CreateTrackbar('Threshold', name, cur_pos, 255, switch_callback)
    
    while True:
        for pt in pts:
            cv.Circle(img, (int(pt[0]),int(pt[1])), radius, green, thickness, connectivity )
        cv.ShowImage('test', img)
        if cv.WaitKey(15) == 27:
            break
    cv.DestroyWindow('test')    
test(image)

# def switch_callback(pos):
#     position = pos
#     if position <= 255 and position >=0:
#         return 'hi'
#     else:
#         return 'hi2'
#         
# def main():
#     imgpath = '/home/wtrdrnkr/Documents/ecog/grids.jpg'
#     img = cv.LoadImageM(imgpath)
#     cv.NamedWindow('Test', flags=cv.CV_WINDOW_AUTOSIZE)
#     cv.CreateTrackbar('Threshold', 'Test', 50, 255, )
#     cv.ShowImage('Test', img)
#     cv.WaitKey(0)
#     print('DONE')
#     
#     # cv.SetTrackbarPos('trackbarName', 'windowName', int(pos)) #?
#     # cv.WaitKey()
#     
# main()