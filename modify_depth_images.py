__author__ = 'Mona Jalal'

import os
import glob
from PIL import Image
import numpy as np
import cv2

CVAR_dataset_path = "C:\\OpenARK_test\\CVAR"
for subdirs, dirs, files in os.walk(CVAR_dataset_path):
    for dir in dirs:
        os.chdir(CVAR_dataset_path +'\\'+dir)
        root_path = CVAR_dataset_path+"\\"+dir
        for depth_file in glob.glob("*_depth.png"):
            im = Image.open(depth_file, 'r')
            width, height = im.size
            pixel_val = list(im.getdata())
            for i in range(len(pixel_val)):
                if (pixel_val[i] == 32001):
                    pixel_val[i] = 0
            np_arr = np.array(pixel_val)
            np_reshaped = np_arr.reshape(height, width)
            modified_depth_file = depth_file[:-4] + '_modified.png'
            cv2.imwrite(modified_depth_file, (np_reshaped).astype(np.uint16))
        os.chdir('..')
