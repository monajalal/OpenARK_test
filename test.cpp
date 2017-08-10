// C++ Libraries
#include <stdio.h>
#include <string>
#include <time.h>

// OpenCV Libraries
#include "opencv2/highgui/highgui.hpp"

// OpenARK Libraries
#include "TestCamera.h"
#include "../OpenARK/Visualizer.h"
#include "../OpenARK/Hand.h"
#include "../OpenARK/Plane.h"
#include "../OpenARK/Calibration.h"
#include "../OpenARK/UDPSender.h"
#include "../OpenARK/Object3D.h"
#include "../OpenARK/StreamingAverager.h"
#include "../OpenARK/global.h"


using namespace cv;

int main(int argc, char** argv) {

	String path_P1 = "C:\\OpenARK_test\\CVAR\\P1\\*_modified.png";
	String path_P3 = "C:\\OpenARK_test\\CVAR\\P3\\*_modified.png";
	//P4 has so much clutter and yields no result as of now
	String path_P4 = "C:\\OpenARK_test\\CVAR\\P4\\*_modified.png";
	String path_P5 = "C:\\OpenARK_test\\CVAR\\P5\\*_modified.png";
	String path_P6 = "C:\\OpenARK_test\\CVAR\\P6\\*_modified.png";
	String path_P7 = "C:\\OpenARK_test\\CVAR\\P7\\*_modified.png";

	std::vector<String> paths = { path_P1, path_P3, path_P4, path_P5, path_P6, path_P7 };
	//std::vector<String> paths = { path_P1, path_P3, path_P5, path_P6, path_P7 };
	//std::vector<String> paths = { path_P3 };
	//std::vector<String> paths = { path_P1, path_P3, path_P5};
	//std::vector<String> paths = { path_P1, path_P3 };

	camera_name = "test";

	DepthCamera * camera = new TestCamera();

	for (auto path : paths) 
	{
		std::vector<String> fn;
		glob(path, fn, false);
		auto starttime = clock();
		auto frame = 0;
		//Calibration::XYZToUnity(*pmd, 4, 4, 3);
		//FileStorage fs;
		//fs.open("RT_Transform.txt", FileStorage::READ);
		//Mat r, t;
		//fs["R"] >> r;
		//fs["T"] >> t;
		//fs.release();
		auto u = UDPSender();
		auto handAverager = StreamingAverager(4, 0.1);
		auto paleeteAverager = StreamingAverager(6, 0.05);

		for (auto filename : fn)
		{
			file_name = filename;
			camera->update();

			// Loading image from sensor
			camera->removeNoise();
			if (camera->badInput) {
				waitKey(10);
			}
			
			// Classifying objects in the scene
			camera->computeClusters(0.02, 500);
			auto clusters = camera->getClusters();
			std::vector<Object3D> objects;
			auto handObjectIndex = -1, planeObjectIndex = -1;
			for (auto i = 0; i < clusters.size(); i++) 
			{
				auto obj = Object3D(clusters[i].clone());

				if (obj.hasHand)
				{
					handObjectIndex = i;
				}

				if (obj.hasPlane)
				{
					planeObjectIndex = i;
				}
				objects.push_back(obj);
			}

			// Interprate the relationship between the objects
			auto clicked = false, paletteFound = false;
			Object3D handObject, planeObject;
			Point paletteCenter(-1. - 1);
			Mat mask = Mat::zeros(camera->getXYZMap().rows, camera->getXYZMap().cols, CV_8UC1);

			if (planeObjectIndex != -1 && handObjectIndex != -1) 
			{
				planeObject = objects[planeObjectIndex];
				handObject = objects[handObjectIndex];

				clicked = handObject.getHand().touchObject(planeObject.getPlane().getPlaneEquation(), planeObject.getPlane().R_SQUARED_DISTANCE_THRESHOLD * 5);
				auto scene = Visualizer::visualizePlaneRegression(camera->getXYZMap(), planeObject.getPlane().getPlaneEquation(), planeObject.getPlane().R_SQUARED_DISTANCE_THRESHOLD, clicked);
				//scene = Visualizer::visualizeHand(scene, handObject.getHand().pointer_finger_ij, handObject.getHand().shape_centroid_ij);
				if (planeObject.leftEdgeConnected)
				{
					Visualizer::visualizePlanePoints(mask, planeObject.getPlane().getPlaneIndicies());
					auto m = moments(mask, false);
					paletteCenter = Point(m.m10 / m.m00, m.m01 / m.m00);
					circle(scene, paletteCenter, 2, Scalar(0, 0, 255), 2);
					paletteFound = true;
				}
				namedWindow("Results", CV_WINDOW_AUTOSIZE);
				imshow("Results", scene);
			}
			else if (handObjectIndex != -1) 
			{
				handObject = objects[handObjectIndex];
				if (os.is_open())
				{
					os << file_name << " "; 
					int num_fingers = handObject.getHand().fingers_xyz.size();
					for (auto i = 0; i <num_fingers ; i++)
					{
						os << FX * (handObject.getHand().fingers_xyz[i][0] / handObject.getHand().fingers_xyz[i][2]) + CX << " " << FY * (handObject.getHand().fingers_xyz[i][1] / handObject.getHand().fingers_xyz[i][2]) + CY << " " << handObject.getHand().fingers_xyz[i][2] * 1000 << " ";
					}
					os << endl;
				}
			}
			else if (planeObjectIndex != -1) 
			{
				planeObject = objects[planeObjectIndex];
				auto scene = Visualizer::visualizePlaneRegression(camera->getXYZMap(), planeObject.getPlane().getPlaneEquation(), planeObject.getPlane().R_SQUARED_DISTANCE_THRESHOLD, clicked);
				if (planeObject.leftEdgeConnected) {
					Visualizer::visualizePlanePoints(mask, planeObject.getPlane().getPlaneIndicies());
					auto m = moments(mask, false);
					paletteCenter = Point(m.m10 / m.m00, m.m01 / m.m00);
					circle(scene, paletteCenter, 2, Scalar(0, 0, 255), 2);
					paletteFound = true;
				}
				namedWindow("Results", CV_WINDOW_AUTOSIZE);
				imshow("Results", scene);
			}

			// Organize the data and send to game engine
			std::string handX = "-", handY = "-", handZ = "-";
			std::string paletteX = "-", paletteY = "-", paletteZ = "-";
			std::string clickStatus = "2";
			std::string num_fingers = "0";
			if (handObjectIndex != -1) 
			{
				auto handPos = handAverager.addDataPoint(objects[handObjectIndex].getHand().fingers_xyz[0]);
				//float hand_pt[3] = { objects[handObjectIndex].getHand().pointer_finger_xyz[0], objects[handObjectIndex].getHand().pointer_finger_xyz[1], objects[handObjectIndex].getHand().pointer_finger_xyz[2]};
				float hand_pt[3] = { handPos[0], handPos[1], handPos[2] };
				auto hand_mat = Mat(3, 1, CV_32FC1, &hand_pt);
				//hand_mat = r*hand_mat + t;
				handX = std::to_string(hand_mat.at<float>(0, 0));
				handY = std::to_string(hand_mat.at<float>(1, 0));
				handZ = std::to_string(hand_mat.at<float>(2, 0));
				num_fingers = std::to_string(objects[handObjectIndex].getHand().fingers_xyz.size());
			}
			else
			{
				handAverager.addEmptyPoint();
			}
			if (paletteFound)
			{
				auto pt = paleeteAverager.addDataPoint(camera->getXYZMap().at<Vec3f>(paletteCenter.y, paletteCenter.x));
				float palette_pt[3] = { pt[0], pt[1], pt[2] };
				auto palette_mat = Mat(3, 1, CV_32FC1, &palette_pt);
				//palette_mat = r*palette_mat + t;
				paletteX = std::to_string(palette_mat.at<float>(0, 0));
				paletteY = std::to_string(palette_mat.at<float>(1, 0));
				paletteZ = std::to_string(palette_mat.at<float>(2, 0));
			}
			else 
			{
				paleeteAverager.addEmptyPoint();
			}
			if (clicked) 
			{
				clickStatus = "1";
			}

			std::string tempS = "";
			tempS = handX + "%" + handY + "%" + handZ + "%" + paletteX + "%" + paletteY + "%" + paletteZ + "%" + clickStatus + "%" + num_fingers;
			u.send(tempS);

			/**** Start: Loop Break Condition ****/
			auto c = waitKey(1);
			if (c == 'q' || c == 'Q' || c == 27) {
				break;
			}
			/**** End: Loop Break Condition ****/
			frame++;
		}
	} //for (String path:paths)

	camera->destroyInstance();
	destroyAllWindows();
	return 0;
}