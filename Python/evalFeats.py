import cv, sys, os
cur_pos = 0;
colorInt = 0;

# Trackbar/switch callback
def switch_callback( position ):
    return 1 #?

def main():
    name = 'evalFeats'
    
    # Point attributes
    radius = 30
    thickness = 2
    connectivity = 8
    green = cv.CV_RGB(0,250,0)
    
    
    src1 = cv.LoadImage('/home/wtrdrnkr/Documents/ecog/grids.jpg')
    

    cv.NamedWindow(name, 1)

    cv.CreateTrackbar( "Threshold", name, cur_pos, 255, switch_callback )
    
    while True:
        pts = [] #list of points returned from featdet
        for pt in pts:
            cv.Circle(src1,pt,radius,green,thickness,connectivity)
        cv.ShowImage(name, src1)
        # Time before change is applied (ms)
        waittime = 15
        if cv.WaitKey( waittime ) == 27: # ESC
            break
    
    cv.DestroyWindow( name )

    return 0

main()
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