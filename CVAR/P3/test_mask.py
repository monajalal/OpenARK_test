import cv2
from PIL import Image
import numpy as np
import glob

for depth_file in glob.glob("*_depth.png"):
    print(depth_file)
    im = Image.open(depth_file, 'r')
    width, height = im.size
    pixel_val = list(im.getdata())

    np_arr = np.array(pixel_val)
    np_reshaped = np_arr.reshape(height, width)
    two_hands_depth_file = depth_file[:6] + '_two_hands_depth.png'
    cv2.imwrite(two_hands_depth_file, (np_reshaped).astype(np.uint16))

    np_reshaped = np_arr.reshape(height, width)

    np_reshaped[:, :115] = 32001


    #modified_depth_file = depth_file[:-4] + '_modified.png'
    cv2.imwrite(depth_file, (np_reshaped).astype(np.uint16))

