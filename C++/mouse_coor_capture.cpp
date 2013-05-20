//#include "stdafx.h"
#include <iostream>
#include <fstream>
#include "opencv\cv.h"
#include "opencv2/highgui/highgui.hpp"

using namespace std;
ofstream myFile;

void mouseEvent(int evt, int x, int y, int flags, void* param){
    if(evt==CV_EVENT_LBUTTONDOWN){
        printf("%d %d\n",x,y);              //displays the mouse coordinates on a command window
  	stringstream ss;
		ss << x;
		string strx = ss.str();

		string myStr="";    
		myStr+=strx;
 
		stringstream ssy;                     
		ssy<<y;
		string stry = ssy.str(); 
		myStr+=" ";
		myStr+=stry;                                //creates a string with all the x and y coordinates of the mouse (with formatting)
		myStr+="\n";
		myFile<<myStr;
	}
}


int main()
{
		myFile.open("CoordinateInfo.txt");
        cvNamedWindow("Mouse Coordinate Calc");   //generate window

        
        cvSetMouseCallback("Mouse Coordinate Calc", mouseEvent, 0);   
        IplImage* img = cvLoadImage("MyPic.jpg");   //load the image
        cvShowImage("Mouse Coordinate Calc", img);
        
        
        cvWaitKey(0);   //wait until a key is entered, or window is closed.
      
        
        cvDestroyWindow("Mouse Coordinate Calc");
        cvReleaseImage(&img);
		myFile.close();
        return 0;
} 
