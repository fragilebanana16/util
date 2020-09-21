#include <iostream>
#include <opencv2/opencv.hpp>
#include <stdlib.h>
#include <stdio.h>
#include <map>
// 实现网格化左上坐标， 十字收集信息， 重复次数统计显示,时延控制单步显示已探测区域,次数文本大小随网格大小动态变化,设计抽象算法类具体实现由子类实现（待完成
using namespace cv;
using namespace std;
#define KEY_TO_STR(ltCoord) to_string(ltCoord.x)+","+to_string(ltCoord.y)
void collect_cross(Mat& aMat, Point p, const int gridSize, vector<Point> pVec);
vector<Point> draw_grid(Mat& aMat, const int divRow, const int divCol, const int imgWidth, const int imgHeight, int& gridSize){
vector<Point> adjacent_coords(Point p, const int gridSize){
/*
                     *--*--*--*---
					 |  |  |  |  |
					 *--*--*--*---
					 |  |  |  |  |
					 -------------
					 A grid on map where we return the left top coords, grid is square as default
					 test case: 2, 4 -> (0,0), (0,1), (0,2), (0,3), (1,0), (1,1), (1,2), (1,3), grid size set to 1
 */
vector<Point> draw_grid(Mat& aMat, const int divRow, const int divCol, const int imgWidth, const int imgHeight, int& gridSize){
	if((0 != imgWidth%divCol) && (0 != imgHeight%divRow)){
		cerr << "Cant divide evenly!" << endl;
		exit(-1);
	}
	gridSize = imgWidth/divCol;
	if(gridSize != imgHeight/divRow){
		cerr << "Can only process square grid!" << endl;
		exit(-1);
	}
    vector<Point> pVec;
	int lt_x;int lt_y;
	for(int r = 0; r < divRow; r++ ){
		lt_y = r*gridSize;
		for(int c = 0; c < divCol; c++ ){
			 // lt pt will never exceed the grid
			lt_x = c*gridSize;
			rectangle(aMat, Point(lt_x, lt_y), Point(lt_x+gridSize-2,lt_y+gridSize-2), Scalar(255,0,0), 1);
			pVec.emplace_back(Point(lt_x, lt_y));
		}
	}     
	return pVec;
}
vector<Point> adjacent_coords(Point p, const int gridSize){
	vector<Point> vec;
	vec.reserve(5);
	vec.emplace_back(Point(p.x, p.y));
	vec.emplace_back(Point(p.x, p.y-gridSize));
	vec.emplace_back(Point(p.x, p.y+gridSize));
	vec.emplace_back(Point(p.x-gridSize, p.y));
	vec.emplace_back(Point(p.x+gridSize, p.y));
	return vec;
}
void collect_cross(Mat aMat, Point p, const int gridSize, vector<Point> pVec, map<string, int>& duplicate_mark){
	for(auto p:pVec){
		if(p.x >= 0 && p.y >=0 && p.x < aMat.cols && p.y < aMat.rows && duplicate_mark[KEY_TO_STR(p)] == 0){ // cut margin
			Mat img_roi = aMat(Rect(p.x, p.y, gridSize, gridSize));
			Mat replace_img(Size(gridSize, gridSize), CV_8UC3, Scalar(255, 255, 255));
			replace_img.copyTo(img_roi);
			duplicate_mark[KEY_TO_STR(p)] += 1;
		}
		else{
			duplicate_mark[KEY_TO_STR(p)] += 1;
		}
	}
}
void plan_A(Mat aMat){
	Mat detected = aMat.clone();
	int m = 0; int n = 0;
    cin >> m >> n;
	int gridSize = 0;
	vector<Point> ltCoords = draw_grid(aMat, m, n, aMat.cols, aMat.rows, gridSize);
	map<string, int> duplicate_mark;
	for(auto ltCoord:ltCoords){
		duplicate_mark.insert(make_pair(to_string(ltCoord.x)+","+to_string(ltCoord.y), 0));
	}
    int t = m*n;
    char map[m][n];
    memset(map, 0, sizeof(map));
    string s;
    vector<string> vec;
    vec.reserve(t);
    while(t){
        cin >> s;
        vec.push_back(s);
        --t;
    }
    char mid[m*n];
    int k=0;
    for(string temp:vec){
        mid[k++] = temp[0];
    }
    int index =0;
    for(int i=0;i<m;i++){
        if(i%2!=0) {
            for(int j=n-1;j>=0;j--){
                map[i][j]=mid[index];index++;
				string s(1,map[i][j]);
				putText(aMat, s, \
				        Point(ltCoords[j+n*i].x+gridSize/2,ltCoords[j+n*i].y+gridSize/2), FONT_HERSHEY_COMPLEX, gridSize/80,\
						cv::Scalar(0, 0, 255), 2, 8, 0);
			    collect_cross(detected, Point(ltCoords[j+n*i]), gridSize, adjacent_coords(Point(ltCoords[j+n*i]), gridSize), duplicate_mark);		  
			    putText(detected, to_string(duplicate_mark[KEY_TO_STR(ltCoords[j+n*i])]), \
				        Point(ltCoords[j+n*i].x+gridSize/2,ltCoords[j+n*i].y+gridSize/2), \
						FONT_HERSHEY_COMPLEX, gridSize/80, cv::Scalar(0, 0, 255), 2, 8, 0);
				imshow("clock", aMat);
				imshow("detected", detected);
	            waitKey(500);
            }
        }
        else{
            for(int j=0;j<n;j++){
                map[i][j]=mid[index];index++;
				string s(1,map[i][j]);
				putText(aMat, s, \
				        Point(ltCoords[j+i*n].x+gridSize/2,ltCoords[j+n*i].y+gridSize/2), FONT_HERSHEY_COMPLEX, gridSize/80,\
						cv::Scalar(0, 0, 255), 2, 8, 0);	
				collect_cross(detected, Point(ltCoords[j+n*i]), gridSize, adjacent_coords(Point(ltCoords[j+n*i]), gridSize), duplicate_mark);		  
			    putText(detected, to_string(duplicate_mark[KEY_TO_STR(ltCoords[j+n*i])]), \
				        Point(ltCoords[j+n*i].x+gridSize/2,ltCoords[j+n*i].y+gridSize/2), \
						FONT_HERSHEY_COMPLEX, gridSize/80, cv::Scalar(0, 0, 255), 2, 8, 0);
				imshow("clock", aMat);
				imshow("detected", detected);
	            waitKey(500);
				
            }
        }
    }
	waitKey(0);
}
int main()
{
	//read the image
    const char* filename = "around_tw.png";
	Mat image = imread(filename);
	if (NULL == image.data){
		cout << "can`t open the file!" << endl;
		exit(-1);
	}
    Mat dst;
    resize(image, dst, Size(400, 400));
	// my route mangement
	plan_A(dst);
	return 0;
}
