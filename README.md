In order to test the OpenARK project, get the OpenARK project by `git clone https://github.com/augcog/OpenARK.git` and the OpenARK_test folder using `git clone https://github.com/monajalal/OpenARK_test.git` and then open the
OpenARK-SDK C++ project from the OpenARK project in Visual Studio (in our case by browsing to C:\OpenARK\OpenARK-SDK and then clicking on **OpenARK-SDK VC++project**). Right click on the **Header Files** and select **Add -> Existing item...** and select the **TestCamera.h** from the **OpenARK_test** folder. Additionally, right click on the Source Files and select Add -> Existing item... and select **test.cpp** and **TestCamera.cpp** from the **OpenARK_test** folder. 
Eventually, right click on the **main.cpp** from the **Source Files** and click on **Remove**. 

The **test.cpp** code depends on the **CVAR** dataset and you can download it from [ICG-Hand Detection and 3D Pose Estimation Website](https://www.tugraz.at/fileadmin/user_upload/Institute/ICG/Downloads/team_lepetit/3d_hand_pose/CVAR_dataset.zip). In our case, **CVAR** dataset exists in **E:\datasets\hand\CVAR** and if you have placed it somewhere else, you should change the paths accordingly right after **int main() {** in **test.cpp** file. 



