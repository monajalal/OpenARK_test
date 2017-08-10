//C++ include files
#include <iostream>
#include <math.h>

//OpenARK include files
#include "../OpenARK/Visualizer.h"
#include "../OpenArk/global.h"

//OpenARK_test files
#include "TestCamera.h"


using namespace std;
using namespace cv;


/***
Private constructor for the tester
***/
TestCamera::TestCamera(bool use_live_sensor): DepthCamera()
{
	depth_width = X_DIMENSION;
	depth_height = Y_DIMENSION;
}

/***
Public deconstructor for the SR300 Camera depth sensor
***/

TestCamera::~TestCamera()
{
	
}

void TestCamera::destroyInstance()
{
	printf("closing sensor\n");

	printf("sensor closed\n");
}

/***
Create xyzMap, zMap, ampMap, and flagMap from sensor input
***/
void TestCamera::update()
{
	
	initilizeImages();
	fillInAmps();
	fillInZCoords();

}

/***
Reads the depth data from the sensor and fills in the matrix
***/
void TestCamera::fillInZCoords()
{	


	vector<Point3f>  xyzBuffer;
	auto depth_image = imread(file_name, IMREAD_ANYDEPTH);
	//if you want to test only a single image uncomment below line
	//auto depth_image = imread("C:\\OpenARK_test\\CVAR\\P3\\000076_depth_modified.png", IMREAD_ANYDEPTH);


	namedWindow("depth", WINDOW_AUTOSIZE);
	imshow("depth", depth_image);

	for (auto v = 0; v < depth_image.rows; v++)
	{
		for (auto u = 0; u < depth_image.cols; u++) 
		{
			auto depth_value = depth_image.at<uint16_t>(v, u);
			Point3f p;
			p.x = ((u - CX)*depth_value*(1.0f / FX)) / 1000.0f;
			p.y = ((v - CY)*depth_value*(1.0f / FY)) / 1000.0f;
			p.z = (depth_value) / 1000.0f;
			xyzBuffer.emplace_back(p);
		}
	}

	xyzMap = Mat(xyzBuffer, true).reshape(3, depth_image.rows);
	auto xyz_mirror = Mat(xyzBuffer, true).reshape(3, depth_image.rows);
	cv::flip(xyz_mirror, xyzMap, 1);
	namedWindow("xyz mirror before", WINDOW_AUTOSIZE);
	imshow("xyz mirror before", xyz_mirror);
}

/***
Reads the amplitude data from the sensor and fills in the matrix
***/
void TestCamera::fillInAmps()
{
	ampMap.data = nullptr;
}

/***
Returns the X value at (i, j)
***/
float TestCamera::getX(int i, int j) const
{
	auto flat = j * depth_width * 3 + i * 3;
	return dists[flat];
}

/***
Returns the Y value at (i, j)
***/
float TestCamera::getY(int i, int j) const
{
	auto flat = j * depth_width * 3 + i * 3;
	return dists[flat + 1];
}

/***
Returns the Z value at (i, j)
***/
float TestCamera::getZ(int i, int j) const
{
	auto flat = j * depth_width * 3 + i * 3;
	return dists[flat + 2];
}

