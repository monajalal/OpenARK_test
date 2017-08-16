__author__ = 'Mona Jalal'

'''
Reads the depth image files and visualizes
all the fingertips on newly created images
'''

import cv2
import itertools
import os
import sys

try:
    CVAR_dataset_path = sys.argv[1]
except IndexError:
    CVAR_dataset_path = ""
    print('You should enter the absolute path to CVAR dataset!')
    sys.exit(1)

for subdirs, dirs, files in os.walk(CVAR_dataset_path):
    for dir in dirs:
        cur_path = CVAR_dataset_path + '\\' + dir
        with open(cur_path + '\\all_fingertips.txt') as fingertips_file:
            for line in fingertips_file:
                points = []
                fingertips_split = line.split(' ')
                depth_image_filename = fingertips_split[0]
                test_image = cv2.imread(cur_path + '\\' + depth_image_filename)
                modified_image = test_image.copy()
                modified_image_name = cur_path + '\\' +depth_image_filename[:-4] + '_all_fingertips.png'
                line_split = ' '.join(fingertips_split[1:]).rstrip()
                line_split = line_split.split(' ')
                iterable = iter(line_split)
                sliced_list = list(iter(lambda: list(itertools.islice(iterable, 2)), []))
                cv2.circle(modified_image, (int(float(sliced_list[0][0])), int(float(sliced_list[0][1]))), 1, (255, 255, 0), -1)
                cv2.circle(modified_image, (int(float(sliced_list[1][0])), int(float(sliced_list[1][1]))), 1, (0, 255, 255), -1)
                cv2.circle(modified_image, (int(float(sliced_list[2][0])), int(float(sliced_list[2][1]))), 1, (0, 255, 0), -1)
                cv2.circle(modified_image, (int(float(sliced_list[3][0])), int(float(sliced_list[3][1]))), 1, (0, 0, 255), -1)
                cv2.circle(modified_image, (int(float(sliced_list[4][0])), int(float(sliced_list[4][1]))), 1, (255, 0, 0), -1)
                cv2.imwrite(modified_image_name,modified_image)