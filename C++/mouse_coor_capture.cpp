//#include "stdafx.h"
#include <iostream>
#include <fstream>
#include "opencv\cv.h"
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/core/core_c.h"
#include "opencv2/core/core.hpp"
#include "opencv2/flann/miniflann.hpp"
#include "opencv2/imgproc/imgproc_c.h"

using namespace std;

/**
* @function main
*/
std::ofstream myFile;
ifstream infile;
IplImage* img;
int posx;
int posy;

void mouseEvent(int evt, int x, int y, int flags, void* param){
    if(evt==CV_EVENT_LBUTTONDOWN){
        //printf("%d %d\n",x,y);
		stringstream ss;
		ss << x;
		string strx = ss.str();

		string myStr="";
		myStr+=strx;

		stringstream ssy;
		ssy<<y;
		string stry = ssy.str();
		myStr+=" ";
		myStr+=stry;
		myStr+="\n";
		myFile<<myStr;
		cvCircle(img,cvPoint(x,y),2,CV_RGB(0,0,255),-1);
		
		cvShowImage("Mouse Coordinate Calc", img);

	}
}


int main(int argc, char** argv)
{
		int popx=0;
		int popy=0;
		string mystring="";
		
		
		
        cvNamedWindow("Mouse Coordinate Calc");

		img = cvLoadImage(argv[1]);
        cvShowImage("Mouse Coordinate Calc", img);
		infile.open(argv[2]);
		if(!infile)
		{

			printf("%s","Cannot find file, assuming unpopulated list.");
		}
		else
		{
			printf("File found. Re-populating image...");
			 while(!infile.eof())
			{
			getline(infile,mystring,' ');
			//printf("%s",mystring);
			posx=atoi(mystring.c_str());
			mystring="";
			printf("%s"," ");
			getline(infile,mystring,'\n');
			//printf("%s",mystring);
			posy=atoi(mystring.c_str());

			//printf("%s","\n");
			
			cvCircle(img,cvPoint(posx,posy),2,CV_RGB(0,0,255),-1);
		
			cvShowImage("Mouse Coordinate Calc", img);
			}

		}
		 myFile.open(argv[2],std::ios_base::app);
        cvSetMouseCallback("Mouse Coordinate Calc", mouseEvent, 0);
        
        
        
        cvWaitKey(0);
      
        
        cvDestroyWindow("Mouse Coordinate Calc");
        cvReleaseImage(&img);
		myFile.close();
        return 0;
} 
