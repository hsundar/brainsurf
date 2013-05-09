import cv, sys, os
# Problems:
# == Cant find feature detection algorithms (python)
# == How to get rid of previous detected pts as trackbar moves

image = cv.LoadImage('/home/michaelm/Documents/ecog/grids.jpg')
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
        pt0 = (cv.GetTrackbarPos('Threshold', name),cv.GetTrackbarPos('Threshold', name))
        pts = [pt0] #list of points returned from feature detection
        for pt in pts:
            cv.Circle(image,pt,radius,green,thickness,connectivity)
        
        cv.ShowImage(name, image)

        # Key to quit
        if cv.WaitKey( 15 ) == 27: # ESC
            break
    
    cv.DestroyWindow( name )

def switch_callback( position ):
    cur_pos = position

main(image)



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