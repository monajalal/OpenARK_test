__author__ = 'Mona Jalal'

'''
Create fingertips file given the joints file in CVAR dataset
'''

import os
import itertools
import sys

try:
    CVAR_dataset_path = sys.argv[1]
except IndexError:
    CVAR_dataset_path = ""
    print('You should enter the absolute path to CVAR dataset!')
    sys.exit(1)

for subdirs, dirs, files in os.walk(CVAR_dataset_path):
    for dir in dirs:
        root_path = CVAR_dataset_path+"\\"+dir
        with open(root_path + "\\" + "joint.txt") as joints_file:
            with open(root_path + "\\" +'fingertips.txt', 'w+') as fingertips_file:
                next(joints_file)
                for line in joints_file:
                    joint_line_split = line.split(' ')
                    depth_image_file = joint_line_split[0][10:]
                    joint_line_split = ' '.join(joint_line_split[1:]).rstrip()
                    joint_line_split = joint_line_split.split(' ')
                    list_of_list = []
                    iterable = iter(joint_line_split)
                    sliced_list = list(iter(lambda: list(itertools.islice(iterable, 3)), []))
                    fingertips = []
                    fingertips.extend((sliced_list[16], sliced_list[12], sliced_list[8], sliced_list[4], sliced_list[20]))
                    flat_list = [item for sublist in fingertips for item in sublist]
                    str_flat_list = " ".join(str(x) for x in flat_list)
                    fingertips_str = depth_image_file+' '+ str_flat_list
                    fingertips_file.write(fingertips_str + "\n")