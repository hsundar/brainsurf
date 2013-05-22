//#include "stdafx.h"
#include <iostream>
#include <fstream>
#include "wtypes.h"
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
int saveit;
int saveity;
boolean isit;
IplImage *myresize;

void mouseEvent(int evt, int x, int y, int flags, void* param){
	int virx=0;
	int viry=0;
    if(evt==CV_EVENT_LBUTTONDOWN){
        //printf("%d %d\n",x,y);
		//pos/oldsize = x/newsize
		if(isit){
		virx=(saveit*x)/(myresize->width);
		viry=(saveity*y)/(myresize->height);
		//printf("\n%d %d\n",virx,viry);
		//printf("Actual: %d %d",x,y);
		}
		stringstream ss;
		if(isit){
			ss<<virx;
		}
		else{
		ss << x;
		}
		string strx = ss.str();

		string myStr="";
		myStr+=strx;

		stringstream ssy;
		if(isit)
		{
			ssy<<viry;
		}
		else{
		ssy<<y;
		}
		string stry = ssy.str();
		myStr+=" ";
		myStr+=stry;
		myStr+="\n";
		myFile<<myStr;

		if(isit)
		{
			cvCircle(myresize,cvPoint(x,y),2,CV_RGB(0,0,255),-1);
			cvShowImage("Mouse Coordinate Calc", myresize);
		}
		else{
		cvCircle(img,cvPoint(x,y),2,CV_RGB(0,0,255),-1);
		
		cvShowImage("Mouse Coordinate Calc", img);
		}
	}
}

void GetDesk(int& horizontal, int& vertical)
{
   RECT desktop;
   // Get a handle to the desktop window
   const HWND hDesktop = GetDesktopWindow();
   // Get the size of screen to the variable desktop
   GetWindowRect(hDesktop, &desktop);
   // The top left corner will have coordinates (0,0)
   // and the bottom right corner will have coordinates
   // (horizontal, vertical)
   horizontal = desktop.right;
   vertical = desktop.bottom;
}


int main(int argc, char** argv)
{
		isit=false;

		int popx=0;
		int popy=0;
		int size=0;
		boolean newfile=false;
		string mystring="";
		
		
		
        

		img = cvLoadImage(argv[1]);
		saveit=img->width;
		saveity=img->height;
		//image resizing
		GetDesk(popx,popy);
		
		if((img->width)>popx)
		{
			printf("Image too big for monitor...resizing\n");
			//img->width=1000;
			isit=true;

		}
		if((img->height)>popy)
		{
			printf("Image too big for monitor...resizing\n");
			//img->height=1000;
			isit=true;
		}
		if(isit)
		{
			myresize = cvCreateImage(cvSize(1000,500),img->depth,img->nChannels);
			cvResize(img,myresize);
			cvShowImage("Mouse Coordinate Calc", myresize);


		}
		cvNamedWindow("Mouse Coordinate Calc",CV_WINDOW_AUTOSIZE);
		if(isit){
        cvShowImage("Mouse Coordinate Calc", myresize);
		}
		else
		{
			cvShowImage("Mouse Coordinate Calc", img);
		}
		infile.open(argv[2]);
		if(!infile)
		{

			printf("%s","Cannot find file, assuming unpopulated list.");
			newfile=true;
		}
		else
		{
			printf("File found. Re-populating image...");
			newfile=false;
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
			if(isit)
			{
				cvCircle(myresize,cvPoint(((posx*myresize->width)/saveit),(posy*myresize->height)/saveity),2,CV_RGB(0,255,255),-1);
				cvShowImage("Mouse Coordinate Calc", myresize);

			}
			else{
				cvCircle(img,cvPoint(posx,posy),2,CV_RGB(0,0,255),-1);
				cvShowImage("Mouse Coordinate Calc", img);
			}
				
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
