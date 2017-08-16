# OpenARK_test

OpenARK_test is an open-source way of testing the OpenARK platform for checking its accuracy for fingertips detection. Currently, OpenARK-test can calculate the accuracy for each folder in CVAR dataset separately as well as the entire CVAR dataset from this [paper](https://www.tugraz.at/fileadmin/user_upload/Institute/ICG/Images/team_lepetit/publications/oberweger_cvpr16.pdf).
In order to test the OpenARK project, get the OpenARK project by `git clone https://github.com/augcog/OpenARK.git` and the OpenARK_test folder using `git clone https://github.com/monajalal/OpenARK_test.git` and then open the
OpenARK-SDK C++ project from the OpenARK project in Visual Studio (in our case by browsing to C:\OpenARK\OpenARK-SDK and then clicking on **OpenARK-SDK VC++project**). Right click on the **Header Files** and select **Add -> Existing item...** and select the **TestCamera.h** from the **OpenARK_test** folder. Additionally, right click on the Source Files and select Add -> Existing item... and select **test.cpp** and **TestCamera.cpp** from the **OpenARK_test** folder. 
Eventually, right click on the **main.cpp** from the **Source Files** and click on **Remove**. 

The **test.cpp** code depends on the **CVAR** dataset and you can download it from [ICG-Hand Detection and 3D Pose Estimation Website](https://www.tugraz.at/fileadmin/user_upload/Institute/ICG/Downloads/team_lepetit/3d_hand_pose/CVAR_dataset.zip). In our case, **CVAR** dataset exists inside the OpenARK_test. <br />

In order to calculate the accuracy on the given CVAR dataset with annotation only for the visible fingertips, execute something like below in the command prompt: <br />
**python compute_accuracy.py "path to CVAR dataset"** 
In above command, the argument to the Python code is the absolute path to the CVAR dataset. In case you want to annotate the dataset manually yourself, run the following scripts in order: <br />


1) create fingertip files out of given CVAR joint files: **python create_fingertips_file.py "path to CVAR dataset"** <br />
2) annotate the visible fingertips **manually using the mouse click: python annotate_visible_fingertips.py "path to CVAR dataset"** <br />
3) visualize all the fingertips: **python vis_all_fingertips.py "path to CVAR dataset"** <br />
4) visualize the visible fingertips: **python vis_visible_fingertips.py "path to CVAR dataset"** <br />


While annotating the fingertips manually, a hand will be shown to you with all the visible and non-visible fingertips. Use the mouse left-click to select a point near the all visible fingertips in each hand and then press ESC/ Enter. At the end of this task, a file named **all_fingertips.txt** and also another file named **visible_fingertips.txt** is created in each folder. The former has all the annotated as well as invisible fingertips location and the latter has 0 and 1 flag values indicating if a fingertip is invisible or visible. In **all_fingertips.txt** file the format is as follows with depth image name in the beginning of the line followed by five fingertips x an y pixel locations: <br />
depth_image_name x y x y x y x y x y <br />
You can see an example below: <br />
000000_depth.png 122 139 145 120 163 113 183 117 224 161 <br />

In **visible_fingertips.txt** file the format is as follows with depth image name in the beginning of the line followed by five binary values indicating if the corresponding fingertip in the **all_fingertips.txt** file is visible (1) or invisible (0). <br />
depth_image_name vis/invis vis/invis vis/invis vis/invis vis/invis <br />
Here's a line example: <br />
000041_depth.png 0 1 1 0 0 <br />

Note: CVAR dataset has folders named P1, P3, P4, P5, P6, and P7. P3 folder includes two hands however only the 21 joints information for the right hand is given. In the modified dataset, we have provided the user with only the depth image for the right hand by masking the left hand. CVAR dataset images are of the resolution 320*240 pixels. The camera intrinsics for the CVAR dataset collected by Creative Senz3D camera is as follows: Fx: 224.501999, Fy: 230.494003, Cx: 160.000000, and Cy: 120.000000. <br />



We have used [**Python3.6**](https://www.continuum.io/downloads) from Continuum Analytics for running the Python scripts. <br />

----

## Credits and references

[Mona Jalal](http://monajalal.com/), [Joseph Menke](https://people.eecs.berkeley.edu/~joemenke/), [Allen Y. Yang](https://people.eecs.berkeley.edu/~yang/), [S. Shankar Sastry](http://robotics.eecs.berkeley.edu/~sastry/).
