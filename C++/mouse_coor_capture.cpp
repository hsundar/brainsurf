
//#include "stdafx.h"
#include <iostream>
#include <stdio.h>
#include <vector>
#include <fstream>
#include <QtDebug>
#include <QMessageBox>
#include <QFileDialog>
#include <QKeyEvent>
#include <QMessageBox>
#include "QApplication"
#include "QDesktopWidget"
#include "opencv\cv.h"
#include "opencv2/core/core.hpp"
#include "opencv2/features2d/features2d.hpp"
#include "opencv2/nonfree/features2d.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/core/core_c.h"
#include "opencv2/core/core.hpp"
#include "opencv2/flann/miniflann.hpp"
#include "opencv2/imgproc/imgproc_c.h"

using namespace std;
using namespace cv;

/**
* @function main
*/
std::ofstream myFile;
ifstream infile;
IplImage* img;
int posx;
int posy;
int saveit;  //the original image's width
int saveity;  //the original image's height
bool generated=false;  //boolean to check if the datapoints were generated by SURF
Mat img1_draw, img2_draw;
bool isit;  //isit is the boolean variable that sees if the picture has been resized when it was loaded.
bool showoriginal=true;
bool labelmode=false; //boolean to check if the program is currently taking user inputs to create the labels for the descriptors
IplImage *myresize;
const char* filepointer;
extern QApplication a;
const char* imagepathholder;
const char* textpathholder;
std::vector<std::string> featurebox;
std::vector<std::string> ignorepoints;
IplImage* returndrawn(Mat img1, std::vector<KeyPoint> keypoints_1, Mat img1_draw, const char* name);

void mouseEvent(int evt, int x, int y, int flags, void* param){
    int virx=0;
    int viry=0;
    if(evt==CV_EVENT_LBUTTONDOWN){
        myFile.open(filepointer,std::ios_base::app);
        if(isit){    //if the picture has been resized,
        virx=(saveit*x)/(myresize->width);   //the actual x coordinate of the actual image is the proportion of the original image's width times its x
                                             //coordinate, divided by the original width.
        viry=(saveity*y)/(myresize->height);
        }
        stringstream ss;   //stringsteam to write into the file
        if(isit){
            ss<<virx;   //write the actual x coordinate into the stringstream
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
        myFile.close();

    }

    if(evt==CV_EVENT_RBUTTONDOWN)
    {
        ifstream mousefile;
        mousefile.open(filepointer);
        bool isitnear = false;  //boolean to check if the mouse pointer is near a keypoint
        float xholder;
        float yholder;
        float nearx=0;
        float neary=0;
        string mousestring;
        virx=(saveit*x)/(myresize->width);   //the actual x coordinate of the actual image is the proportion of the original image's width times its x
                                             //coordinate, divided by the original width.
        viry=(saveity*y)/(myresize->height);
        while(!mousefile.eof())
       {
           getline(mousefile,mousestring,' ');
           xholder=atof(mousestring.c_str());
           mousestring="";
           getline(mousefile,mousestring,'\n');
           yholder=atof(mousestring.c_str());
           if((((x>xholder-3)&&(x<xholder+3))&&((y>yholder-3)&&(y<yholder+3)))&&(!isit))
           {
               isitnear=true;
               nearx=xholder;
               neary=yholder;
               QMessageBox askBox;
               askBox.setWindowTitle("Point deletion confirmation");
               askBox.setText("Are you sure you want to delete these points?");
               askBox.setStandardButtons(QMessageBox::Ok | QMessageBox::Cancel);
               askBox.setDefaultButton(QMessageBox::Ok);
               QString xcoor=QString::number(xholder);
               QString ycoor=QString::number(yholder);
               xcoor.append(" ");
               xcoor.append(ycoor);
               xcoor.append("\n");
               askBox.setInformativeText(xcoor);
               int choice=askBox.exec();
               string holderstring;
               holderstring=xcoor.toStdString();
               //holderstring.append("\n");
               if(labelmode)
               {
                   ignorepoints.push_back(xcoor.toStdString());
               }
               mousefile.close();
               if(choice==QMessageBox::Ok)
               {
                   ifstream readsize;
                   readsize.open(filepointer);
                   if(!readsize){
                       qDebug()<<"ERROR";
                   }
                   qDebug()<<"Part 0";
                   int size=0;
                   string holderstr;
                   for(int i=0;readsize>>holderstr;i++)
                   {
                        size++;
                        qDebug()<<i;

                   }
                  readsize.close();

                  vector<string> pointarray;

                  ifstream readfile;
                  readfile.open(filepointer);

                  string mainholder;
                  for(int i=0;i<size;i++)
                  {
                      getline(readfile,mainholder,'\n');

                      mainholder.append("\n");
                      qDebug()<<QString(mainholder.c_str())<<QString(holderstring.c_str());
                      qDebug()<<"end";
                      if(mainholder.compare(holderstring)==0)
                      {
                          mainholder="";
                      }
                      pointarray.push_back(mainholder);
                  }
                  readfile.close();
                  if(remove(filepointer) !=0)
                  {
                          qDebug()<<"error with deletion.";
                  }

                  ofstream writefile;
                  writefile.open(filepointer,std::ios_base::app);
                  for(int i=0;i<pointarray.size();i++)
                  {
                      writefile<<pointarray[i];
                  }
                  writefile.close();
                   QMessageBox confirmBox;
                   confirmBox.setWindowTitle("Point deleted.");
                   confirmBox.setText("The point has been deleted.");
                   confirmBox.setStandardButtons(QMessageBox::Ok);
                   confirmBox.setDefaultButton(QMessageBox::Ok);
                   confirmBox.exec();
               }
           }
           else if((((virx>xholder-30)&&(virx<xholder+30))&&((viry>yholder-30)&&(viry<yholder+30)))&&(isit))
           {
               qDebug()<<"Launched";
               isitnear=true;
               nearx=xholder;
               neary=yholder;
               QMessageBox askBox;
               askBox.setWindowTitle("Point deletion confirmation");
               askBox.setText("Are you sure you want to delete these points?");
               askBox.setStandardButtons(QMessageBox::Ok | QMessageBox::Cancel);
               askBox.setDefaultButton(QMessageBox::Ok);
               QString xcoor=QString::number(xholder);
               QString ycoor=QString::number(yholder);
               xcoor.append(" ");
               xcoor.append(ycoor);
               xcoor.append("\n");
               askBox.setInformativeText(xcoor);
               int choice=askBox.exec();
               string holderstring;
               holderstring=xcoor.toStdString();

               if(labelmode)
               {
                   ignorepoints.push_back(xcoor.toStdString());
               }
               mousefile.close();
               if(choice==QMessageBox::Ok)
               {
                   ifstream readsize;
                   readsize.open(filepointer);
                   if(!readsize){
                       qDebug()<<"ERROR";
                   }
                   qDebug()<<"Part 0";
                   int size=0;
                   string holderstr;
                   for(int i=0;readsize>>holderstr;i++)
                   {
                        size++;
                        qDebug()<<i;

                   }
                  readsize.close();

                  vector<string> pointarray;

                  ifstream readfile;
                  readfile.open(filepointer);

                  string mainholder;
                  for(int i=0;i<size;i++)
                  {
                      getline(readfile,mainholder,'\n');

                      mainholder.append("\n");
                      if(mainholder.compare(holderstring)==0)
                      {
                          mainholder="";
                      }
                      qDebug()<<"Part this one";
                      pointarray.push_back(mainholder);
                  }
                  readfile.close();
                  if(remove(filepointer) !=0)
                  {
                          qDebug()<<"error with deletion.";
                  }

                  ofstream writefile;
                  writefile.open(filepointer,std::ios_base::app);
                  for(int i=0;i<pointarray.size();i++)
                  {
                      writefile<<pointarray[i];
                  }
                  writefile.close();
                   QMessageBox confirmBox;
                   confirmBox.setWindowTitle("Point deleted.");
                   confirmBox.setText("The point has been deleted.");
                   confirmBox.setStandardButtons(QMessageBox::Ok);
                   confirmBox.setDefaultButton(QMessageBox::Ok);
                   confirmBox.exec();
               }

           }

       }
        if(isitnear)
        {
            qDebug()<<"Mouse Event!"<<nearx<<neary;
        }
        else
        {
            qDebug()<<"No Mouse Event!";
        }

    }
 }

int* GetDesk()  //function to get the properties of the screen
{
    //QApplication a(argc,argv);
    const int width = QApplication::desktop()->width();
    const int height = QApplication::desktop()->height();
    const QRect rect = QApplication::desktop()->rect();

    const int left = rect.left();
    const int right = rect.right();
    const int bottom = rect.bottom();
    const int top = rect.top();
    int intholder[2];
    intholder[0]=width;
    intholder[1]=height;
    int* point;   //pointer to the array containing the information
    point=&intholder[0];
    return point;  //points to the array of information, the first element is the width, the second is the height
}


int OpenCVMain(const char* direcimg, const char* directxt, const char* featpath, int minHessian, QFileInfoList filelist,int curIndex)
{
        filepointer=directxt;
        isit=false;  //assume that the image is not resized, initially.
        bool newfile=false;     //assume that the a new text file is not needed initially
        string mystring="";


        //img = cvLoadImage(argv[1]);
        img=cvLoadImage(direcimg);  //Iplimage object that contains the desired image
        saveit=img->width;      //get the image's properties
        saveity=img->height;
        //image resizing
       int popx=(GetDesk())[0];   //size of the screen (x)-->width
       int popy=(GetDesk())[1];   //size of the screen (y)-->height

        //proportion calculations
        float px=0.00;  //ratio of image to screen width
        float py=0.00;  //ratio of image to screen length
        float maxp=0.00;  // the maximum of the two ratios
        //calculation to see if the image's proportions are larger than the screen
        px=(float)saveit/(float)popx;  //get the image's ratio/screen ratio
        py=(float)saveity/(float)popy;
        maxp=max(px,py);  //max of the two ratios

        if(maxp>1)   //if any of the two ratios are larger than 1 (if any image is larger than the screen)
        {
            isit=true;   //the image has to be resized.
        }
        else
        {
            isit=false;   // the image does not have to be resized.
        }

        cvNamedWindow("Mouse Coordinate Calc",CV_WINDOW_AUTOSIZE);  //create the named window


        if(isit)
        {
            myresize=cvCreateImage(cvSize((saveit/maxp),(saveity/maxp)),img->depth,img->nChannels); //create a new resized image with the                                                                                          //original image's properties, but
                                                                                                    //with the new proportions
            cvResize(img,myresize);   //resize the image.
        }
        if(isit){   //if as resize event has taken place,
        cvShowImage("Mouse Coordinate Calc", myresize);   //show the resized image.
        }
        else  //if not
        {
            cvShowImage("Mouse Coordinate Calc", img);  //show the orignial image
        }

        infile.open(directxt);  //attempt to open the appropriate textfile that was passed as a second parameter (the url).
        if(!infile)  //if the appropriate text file is not created, generate the points
        {

            printf("%s",direcimg);
            newfile=true;
            QMessageBox msgBox;
            msgBox.setText("Appropriate text file not found. Press 'g' to generate points automatically.");
            msgBox.setStandardButtons(QMessageBox::Ok);
            msgBox.setDefaultButton(QMessageBox::Ok);

            msgBox.exec();

        }
        else  //if the textfile does exist, draw the points contained in the textfile onto the screen
        {
            printf("File found. Re-populating image...");
            newfile=false;
             while(!infile.eof())
            {
                getline(infile,mystring,' ');

                posx=atoi(mystring.c_str());
                mystring="";
                printf("%s"," ");
                getline(infile,mystring,'\n');

                posy=atoi(mystring.c_str());


                if(isit)
                {
                    cvCircle(myresize,cvPoint(((posx*myresize->width)/img->width),(posy*myresize->height)/img->height),2,CV_RGB(0,0,255),-1);
                    cvShowImage("Mouse Coordinate Calc", myresize);

                }
                else{
                    cvCircle(img,cvPoint(posx,posy),2,CV_RGB(0,0,255),-1);
                    cvShowImage("Mouse Coordinate Calc", img);
                }

            }
            infile.close();
            cvSetMouseCallback("Mouse Coordinate Calc", mouseEvent, 0);

        }
        cvSetMouseCallback("Mouse Coordinate Calc", mouseEvent, 0);
        int keypressed=cvWaitKey(0);
        qDebug()<<keypressed;
        if(keypressed=='d'){
            curIndex+=1;
            curIndex=curIndex%filelist.size();
            QString QImagePath=filelist[curIndex].absoluteFilePath();
            QByteArray holder = QImagePath.toLocal8Bit();
            const char* ImagePath = holder.data();

            QString QTxtPath=QImagePath;
            QTxtPath.append(".txt");
            QByteArray holder2 = QTxtPath.toLocal8Bit();
            const char* TxtPath = holder2.data();

            OpenCVMain(ImagePath,TxtPath,featpath,minHessian,filelist,curIndex);

        }
        if(keypressed=='a')
        {
            curIndex-=1;
            if(curIndex<0)
            {
                curIndex=filelist.size()-1;
            }
            QString QImagePath=filelist[curIndex].absoluteFilePath();
            QByteArray holder = QImagePath.toLocal8Bit();
            const char* ImagePath = holder.data();

            QString QTxtPath=QImagePath;
            QTxtPath.append(".txt");
            QByteArray holder2 = QTxtPath.toLocal8Bit();
            const char* TxtPath = holder2.data();

            OpenCVMain(ImagePath,TxtPath,featpath,minHessian,filelist,curIndex);
        }
        if(keypressed==27)
        {
            cvDestroyWindow("Mouse Coordinate Calc");
            cvReleaseImage(&img);
            return 0;
        }
        if(keypressed=='g')
        {
            std::vector<std::string> offloader;
            printf("%s",direcimg);
            newfile=true;
            QMessageBox msgBox;
            msgBox.setText("Generating points...");
            msgBox.setStandardButtons(QMessageBox::Ok);
            msgBox.setDefaultButton(QMessageBox::Ok);
            msgBox.exec();
            Mat img_1;
            if(isit){
                img_1=myresize;
            }
            else{
                img_1 = imread( direcimg, CV_LOAD_IMAGE_GRAYSCALE );
            }
            if( !img_1.data)
            { std::cout<< " --(!) Error reading images " << std::endl; return -1; }            ;

            SiftFeatureDetector detector( minHessian );

            std::vector<KeyPoint> keypoints_1;

            detector.detect( img_1, keypoints_1 );

            //-- Draw keypoints
            Mat img1_keys;

            drawKeypoints( img_1, keypoints_1, img1_keys, Scalar::all(-1), DrawMatchesFlags::DEFAULT );

            if(isit){
                IplImage* image2=cvCloneImage(&(IplImage)img1_keys);
                myresize=image2;
                cvShowImage("Mouse Coordinate Calc", myresize);
                std::ofstream tempfile;
                tempfile.open(directxt,std::ios_base::app);
                for(std::vector<KeyPoint>::iterator it = keypoints_1.begin(); it != keypoints_1.end(); ++it) {
                    stringstream string1 (stringstream::in | stringstream::out);
                    float tempholder=0.00;
                    float finalholder=0.00;
                    tempholder=keypoints_1.at(it - keypoints_1.begin()).pt.x;
                    finalholder=(saveit*tempholder)/(myresize->width);
                    string1<<finalholder;
                    string1<<" ";
                    tempholder=keypoints_1.at(it - keypoints_1.begin()).pt.y;
                    finalholder=(saveity*tempholder)/(myresize->height);
                    string1<<finalholder;
                    string1<<"\n";
                    string offload=string1.str();
                    tempfile<<offload;
                    offloader.push_back(offload);
                }
                tempfile.close();
                qDebug()<<"Works until here";
            }
            else{
                IplImage* image2=cvCloneImage(&(IplImage)img1_keys);
                img=image2;
                cvShowImage("Mouse Coordinate Calc", img);
                std::ofstream tempfile;
                tempfile.open(directxt,std::ios_base::app);
                for(std::vector<KeyPoint>::iterator it = keypoints_1.begin(); it != keypoints_1.end(); ++it) {
                    stringstream string1 (stringstream::in | stringstream::out);
                    string1<<keypoints_1.at(it - keypoints_1.begin()).pt.x;
                    string1<<" ";
                    string1<<keypoints_1.at(it - keypoints_1.begin()).pt.y;
                    string1<<"\n";
                    string offload=string1.str();
                    tempfile<<offload;
                    offloader.push_back(offload);
                }
                tempfile.close();
                qDebug()<<"Worked";
            }
            //logic to start creating the feature file
            qDebug()<<featpath;
            std::ofstream featurefile;
            featurefile.open(featpath,std::ios_base::app);
            qDebug()<<"Please provide modifications and then press enter.";
            vector<float*> descriptors;
            labelmode=true;
            if(!isit)
            {
                //SIFT::operator()(img_1,keypoints_1, descriptors,true);  //DEBUG THIS LINE
                SiftDescriptorExtractor extractor;
                Mat descriptors_1;
                extractor.compute( img_1, keypoints_1, descriptors_1 );
                int size=keypoints_1.size();
                qDebug()<<"Works until here for now"<<size;
                //std::cout<<descriptors_1.row(1);
                //std::cout<<descriptors_1.row(2);
                for(int rowit=0; rowit<descriptors_1.rows;rowit++)
                {
                    string line;
                    stringstream linecreator;
                    linecreator<<"T"<<" ";
                    for(int colit=0; colit<descriptors_1.cols;colit++)
                    {
                        linecreator<<descriptors_1.at<double>(rowit,colit)<<" ";
                    }
                    linecreator<<"\n";
                    line=linecreator.str();
                    featurebox.push_back(line);
                }
                qDebug()<<"Press any key once you get done with the changes.";
                cvSetMouseCallback("Mouse Coordinate Calc", mouseEvent, 0);
                cvWaitKey(0);

                for(std::vector<std::string>::iterator it = offloader.begin(); it != offloader.end(); ++it) {
                    for(std::vector<std::string>::iterator it2 = ignorepoints.begin(); it2 != ignorepoints.end(); ++it2) {
                        string compar1=*it;
                        string compar2=*it2;
                        std::cout<<compar1<<compar2;
                        //std::cout<<*it;
                        if(compar1.compare(compar2)==0)
                        {

                            std::cout<<"DETECTED!";
                            int indexof=it - offloader.begin();
                            string manipulator=featurebox[indexof];
                            std::replace(manipulator.begin(),manipulator.end(),'T','F');
                            featurebox[indexof]=manipulator;

                        }

                    }

                }
                for(std::vector<string>::iterator it = featurebox.begin(); it != featurebox.end(); ++it) {
                    featurefile<<*it;
                }

                featurefile.close();
                labelmode=false;
            }

            OpenCVMain(direcimg,directxt,featpath,minHessian,filelist,curIndex);


        }

        cvDestroyWindow("Mouse Coordinate Calc");
        cvReleaseImage(&img);
        return 0;
}










//Previous versions.
//snip saves:
/*
//currently only supports one mode
int minHessian=400;
Mat img1 = imread(direcimg,CV_LOAD_IMAGE_GRAYSCALE);
Mat img2 = imread(direcimg,CV_LOAD_IMAGE_GRAYSCALE);
//cv::SurfFeatureDetector detector = cv::SURF(minHessian,4,2,true,false);
SurfFeatureDetector detector=cv::SURF(minHessian,4,2,true,false);
std::vector<KeyPoint> keypoints_1;
newfile=true;
//create a material using the image

detector.detect(img1,keypoints_1);

cvWaitKey(100);
*/
/*
if(isit)
{
    //drawKeypoints( img1, keypoints_1, img1_draw, Scalar::all(-1), DrawMatchesFlags::DEFAULT );
    //IplImage* image2=cvCloneImage(&(IplImage)img1_draw);
    //myresize=image2;

}
else
{
    //img=returndrawn(img1,keypoints_1,img1_draw,"Mouse Coordinate Calc");
        /*
        cv::FileStorage fs(directxt, cv::FileStorage::WRITE);
        write(fs,"anameyoulike",keypoints_1);
        QMessageBox msgBox2;
        msgBox2.setText("Points written to file.");
        msgBox2.setStandardButtons(QMessageBox::Ok);
        msgBox2.setDefaultButton(QMessageBox::Ok);

        msgBox2.exec();
        generated=true;*//*
}
*/

/* Extracted from not finding the textfile part:
 *Mat img_1;
            if(isit){
                img_1=myresize;
            }
            else{
                img_1 = imread( direcimg, CV_LOAD_IMAGE_GRAYSCALE );
            }
            if( !img_1.data)
            { std::cout<< " --(!) Error reading images " << std::endl; return -1; }            ;

            SiftFeatureDetector detector( minHessian );

            std::vector<KeyPoint> keypoints_1;

            detector.detect( img_1, keypoints_1 );

            //-- Draw keypoints
            Mat img1_keys;

            drawKeypoints( img_1, keypoints_1, img1_keys, Scalar::all(-1), DrawMatchesFlags::DEFAULT );

            if(isit){
                IplImage* image2=cvCloneImage(&(IplImage)img1_keys);
                myresize=image2;
                cvShowImage("Mouse Coordinate Calc", myresize);
                std::ofstream tempfile;
                tempfile.open(directxt,std::ios_base::app);
                for(std::vector<KeyPoint>::iterator it = keypoints_1.begin(); it != keypoints_1.end(); ++it) {
                    stringstream string1 (stringstream::in | stringstream::out);
                    float tempholder=0.00;
                    float finalholder=0.00;
                    tempholder=keypoints_1.at(it - keypoints_1.begin()).pt.x;
                    finalholder=(saveit*tempholder)/(myresize->width);
                    string1<<finalholder;
                    string1<<" ";
                    tempholder=keypoints_1.at(it - keypoints_1.begin()).pt.y;
                    finalholder=(saveity*tempholder)/(myresize->height);
                    string1<<finalholder;
                    string1<<"\n";
                    string offload=string1.str();
                    tempfile<<offload;
                }
                tempfile.close();
                qDebug()<<"Worked.";
            }
            else{
                IplImage* image2=cvCloneImage(&(IplImage)img1_keys);
                img=image2;
                cvShowImage("Mouse Coordinate Calc", img);
                std::ofstream tempfile;
                tempfile.open(directxt,std::ios_base::app);
                qDebug()<<"This worked.";
                for(std::vector<KeyPoint>::iterator it = keypoints_1.begin(); it != keypoints_1.end(); ++it) {
                    stringstream string1 (stringstream::in | stringstream::out);
                    string1<<keypoints_1.at(it - keypoints_1.begin()).pt.x;
                    string1<<" ";
                    string1<<keypoints_1.at(it - keypoints_1.begin()).pt.y;
                    string1<<"\n";
                    string offload=string1.str();
                    tempfile<<offload;
                }
                tempfile.close();
                qDebug()<<"Worked";
            }
*/
/* taken from below this:
 cvSetMouseCallback("Mouse Coordinate Calc", mouseEvent, 0);
            int keypressed=waitKey(0);

            if(keypressed=='d'){
                curIndex+=1;
                curIndex=curIndex%filelist.size();
                QString QImagePath=filelist[curIndex].absoluteFilePath();
                QByteArray holder = QImagePath.toLocal8Bit();
                const char* ImagePath = holder.data();

                QString QTxtPath=QImagePath;
                QTxtPath.append(".txt");
                QByteArray holder2 = QTxtPath.toLocal8Bit();
                const char* TxtPath = holder2.data();

                OpenCVMain(ImagePath,TxtPath,featpath, minHessian,filelist,curIndex);

            }
            if(keypressed=='a')
            {
                curIndex-=1;
                if(curIndex<0)
                {
                    curIndex=filelist.size()-1;
                }
                QString QImagePath=filelist[curIndex].absoluteFilePath();
                QByteArray holder = QImagePath.toLocal8Bit();
                const char* ImagePath = holder.data();

                QString QTxtPath=QImagePath;
                QTxtPath.append(".txt");
                QByteArray holder2 = QTxtPath.toLocal8Bit();
                const char* TxtPath = holder2.data();

                OpenCVMain(ImagePath,TxtPath,featpath, minHessian,filelist,curIndex);
            }
            if(keypressed==27)
            {
                cvDestroyWindow("Mouse Coordinate Calc");
                cvReleaseImage(&img);
                return 0;
            }
            cvDestroyWindow("Mouse Coordinate Calc");
            cvReleaseImage(&img);
            return 0;
        }
        */
