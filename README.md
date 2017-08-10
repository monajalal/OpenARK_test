# OpenARK_test

OpenARK_test is an open-source way of testing the OpenARK platform for checking its accuracy for fingertips detection. Currently, OpenARK-test can calculate the accuracy for each folder in CVAR dataset separately as well as the entire CVAR dataset from this [paper](https://www.tugraz.at/fileadmin/user_upload/Institute/ICG/Images/team_lepetit/publications/oberweger_cvpr16.pdf).
In order to test the OpenARK project, get the OpenARK project by `git clone https://github.com/augcog/OpenARK.git` and the OpenARK_test folder using `git clone https://github.com/monajalal/OpenARK_test.git` and then open the
OpenARK-SDK C++ project from the OpenARK project in Visual Studio (in our case by browsing to C:\OpenARK\OpenARK-SDK and then clicking on **OpenARK-SDK VC++project**). Right click on the **Header Files** and select **Add -> Existing item...** and select the **TestCamera.h** from the **OpenARK_test** folder. Additionally, right click on the Source Files and select Add -> Existing item... and select **test.cpp** and **TestCamera.cpp** from the **OpenARK_test** folder. 
Eventually, right click on the **main.cpp** from the **Source Files** and click on **Remove**. 

The **test.cpp** code depends on the **CVAR** dataset and you can download it from [ICG-Hand Detection and 3D Pose Estimation Website](https://www.tugraz.at/fileadmin/user_upload/Institute/ICG/Downloads/team_lepetit/3d_hand_pose/CVAR_dataset.zip). In our case, **CVAR** dataset exists in **E:\datasets\hand\CVAR** and if you have placed it somewhere else, you should change the paths accordingly right after **int main() {** in **test.cpp** file.

In order to calculate the accuracy on the given CVAR dataset with annotation only for the visible fingertips, execute something like below:
**C:\OpenARK_test>python compute_accuracy.py C:\OpenARK_test\CVAR** 
In above command, the argument to the Python code is the absolute path to the CVAR dataset. In case you want to annotate the dataset manually yourself, run the following scripts:

#modify the depth images to convert all zero values to 32001
python modify_depth_images.py
#create fingertip files out of given CVAR joint files
python create_fingertips_file.py
#annotate the visible fingertips manually using the mouse click
python annotate_visible_fingertips.py
#visualize all the fingertips
python vis_all_fingertips.py
#visualize the visible fingertips
python vis_visible_fingertips.py

While annotating the fingertips manually, a hand will be shown to you with all the visible and non-visible fingertips. Use the mouse left-click to select a point near the all visible fingertips in each hand and then press ESC/ Enter. At the end of this task, a file named **all_fingertips.txt** and also another file named **visible_fingertips.txt** is created in each folder. The former has all the annotated as well as invisible fingertips location and the latter has 0 and 1 flag values indicating if a fingertip is invisible or visible. 

P.S.: CVAR dataset has folders named P1, P3, P4, P5, P6, and P7. P3 folder includes two hands however only the 21 joints information for the right hand is given. In the modified dataset, we have provided the user with only the depth image for the right hand by masking the left hand.



We have used [**Python3.6**](https://www.continuum.io/downloads) from Continuum Analytics for running the Python scripts.

----

## Credits and references

Mona Jalal, Joseph Menke, Allen Y. Yang, S. Shankar Sastry.



