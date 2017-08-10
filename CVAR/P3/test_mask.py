import cv2
from PIL import Image
import numpy as np
import glob

for depth_file in glob.glob("*_depth.png"):
    im = Image.open(depth_file, 'r')
    width, height = im.size
    pixel_val = list(im.getdata())

    print(pixel_val)
    np_arr = np.array(pixel_val)
    np_reshaped = np_arr.reshape(height, width)

    for i in range(len(pixel_val)):
        if (pixel_val[i] == 32001):
            pixel_val[i] = 0
    np_arr = np.array(pixel_val)

    np_reshaped = np_arr.reshape(height, width)

    np_reshaped[:, :115] = 0

    modified_depth_file = depth_file[:-4] + '_modified.png'
    cv2.imwrite(modified_depth_file, (np_reshaped).astype(np.uint16))


    print(np_reshaped)

