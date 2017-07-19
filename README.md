In order to test the OpenARK project, get the OpenARK_test folder using https://github.com/monajalal/OpenARK_test.git and then open the
OpenARK-SDK C++ project in Visual Studio (in our case by browsing to C:\OpenARK\OpenARK-SDK and then clicking on OpenARK-SDK VC++project). Right click on the Header Files and select Add -> Existing item... and select the TestCamera.h from the OpenARK_test folder. Additionally, right click on the Source Files and select Add -> Existing item... and select test.cpp and TestCamera.cpp from the OpenARK_test folder. 
Eventually, right click on the main.cpp from the Source Files and click on Remove. 

The test.cpp code depends on the CVAR benchmark and you can download it from [ICG-Hand Detection and 3D Pose Estimation Website](https://www.tugraz.at/fileadmin/user_upload/Institute/ICG/Downloads/team_lepetit/3d_hand_pose/CVAR_dataset.zip) 



