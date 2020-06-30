// compare raw.jpg with other imgs under the current dir
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include <iostream>
#include <io.h>
#include <string>
#include <vector>
#include <cstdlib>
#include <sstream>  
using namespace std;
using namespace cv;
int compare(string &a,string &b)
{
    Mat srcImage_base, hsvImage_base;
	Mat srcImage_test1, hsvImage_test1;
	Mat srcImage_test2, hsvImage_test2;
   
	srcImage_base = imread(a, 1);//base
	srcImage_test1 = imread(b, 1);//test

	//imshow("base", srcImage_base);
	//imshow("test", srcImage_test1);
	
	cvtColor(srcImage_base, hsvImage_base, COLOR_BGR2HSV);
	cvtColor(srcImage_test1, hsvImage_test1, COLOR_BGR2HSV);

	int h_bins = 50; int s_bins = 60;
	int histSize[] = { h_bins, s_bins };
	// hue 0-256, saturation 0-180
	float h_ranges[] = { 0, 256 };
	float s_ranges[] = { 0, 180 };
	const float* ranges[] = { h_ranges, s_ranges };
	
	int channels[] = { 0, 1 };
 
	
	MatND baseHist;
	MatND testHist1;
	
	calcHist(&hsvImage_base, 1, channels, Mat(), baseHist, 2, histSize, ranges, true, false);
	normalize(baseHist, baseHist, 0, 1, NORM_MINMAX, -1, Mat());
	calcHist(&hsvImage_test1, 1, channels, Mat(), testHist1, 2, histSize, ranges, true, false);
	normalize(testHist1, testHist1, 0, 1, NORM_MINMAX, -1, Mat());
	int compare_method = 1;
	double base_base = compareHist(baseHist, baseHist, 2);
	double base_text1 = compareHist(baseHist, testHist1, 2);
	
	cout << "src compareHist:" << base_base << endl;
	cout << "test compareHist:" << base_text1 << endl;
    // if less than ten,consider matched
	if (fabs(base_base-base_text1)<5)
	{
		//cout << "Matched" << endl;
        return 1;
	}
	else
	{
		///cout << "Not Matched" << endl;
        return 0;
	}
	
}

int main()
{
    int i = 132;
    stringstream stream;
    string str;
    // raw img to compare
    string raw = "raw.jpg";
    // match time counter
    int counter  = 0;
    // iter 9 imgs to compare
    for(int i=1;i<11;i++)
    {
        stream << i;
        stream >> str;
        str.append(".jpg");
        counter += compare(str,raw);
        //cout<<str<<endl;
        stream.clear();
    }
    cout<<counter<<" times matched!"<<endl;
	waitKey(0);
	return 0;
}
