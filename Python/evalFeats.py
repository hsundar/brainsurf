import cv, sys, os
g_switch_value = 0;
colorInt = 0;

# Trackbar/switch callback
def switch_callback( position ):
    if position == 0:
         colorInt = 0
    else:
         colorInt = 1

def main():
    name = "Demo Window"
    radius = 30
    thickness = 2
    connectivity = 8
    green = cv.CV_RGB(0,250,0)
    orange = cv.CV_RGB(250,150,0)

    src1 = cv.LoadImage( '/home/wtrdrnkr/Documents/ecog/grids.jpg' )
    pt2 = (100,100)

    cv.NamedWindow( name, 1 )

    cv.CreateTrackbar( "Switch", name, g_switch_value, 1, switch_callback )


    while True:
        if colorInt == 0:
            cv.Circle(src1,pt2,radius,green,thickness,connectivity)
        else:
            cv.Circle(src1,pt2,radius,orange,thickness,connectivity)
        cv.ShowImage(name, src1)
        if cv.WaitKey( 15 ) == 27: 
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