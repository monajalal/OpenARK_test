#pragma once
// OpenCV Libraries
#include <opencv2/opencv.hpp>

// OpenARK Libraries
#include "../OpenARK/DepthCamera.h"

//using namespace Intel::RealSense;

/**
* Class defining the behavior of an SR300 Camera.
* Example on how to read from sensor and visualize its output
* @include SensorIO.cpp
*/
class TestCamera : public DepthCamera
{
public:

	/**
	* Public constructor initializing the SR300 Camera.
	* @param use_live_sensor uses input from real sensor if TRUE. Otherwise reads from input file. Default is set to TRUE.
	*/
	explicit TestCamera(bool use_live_sensor = true);

	/**
	* Deconstructor for the SR300 Camera.
	*/
	~TestCamera();

	/**
	* Gets new frame from sensor.
	* Updates xyzMap, ampMap, and flagMap. Resets clusters.
	*/
	
	void fillInZCoords();

	/**
	* Gracefully closes the SR300 camera.
	*/
	void destroyInstance() override;
	void update();

private:
	/**
	* Getter method for the x-coordinate at (i,j).
	* @param i ith row
	* @param j jth column
	* @return x-coodinate at (i,j)
	*/
	float getX(int i, int j) const;

	/**
	* Getter method for the x-coordinate at (i,j).
	* @param i ith row
	* @param j jth column
	* @return x-coodinate at (i,j)
	*/
	float getY(int i, int j) const;

	/**
	* Getter method for the x-coordinate at (i,j).
	* @param i ith row
	* @param j jth column
	* @return x-coodinate at (i,j)
	*/
	float getZ(int i, int j) const;


	/**
	* Update the values in the ampMap.
	*/
	void fillInAmps();

	//Private Variables
	float* dists;
	float* amps;
	cv::Mat frame;
	const int depth_fps = 30;
	int depth_width;
	int depth_height;
	cv::Size bufferSize;
	
};