__author__ = "Mona Jalal"

'''
Given the CVAR visible fingertips and the fingertips
annotated by OpenARK, calculates the accuracy per folder
in CVAR dataset as well as overall among all folders.
'''

import itertools
import math
from PIL import Image
import numpy as np
import cv2
import glob
import os
import itertools
import linecache
import subprocess
import sys


total_correct_fingertips_count = 0
total_CVAR_fingertips = 0
per_folder_correct_fingertips_count = {}
per_folder_accuracy = {}
openark_files = glob.glob("CVAR_folders\\*.txt")
#CVAR_dataset_path = "C:\\OpenARK_test\\CVAR"

try:
    CVAR_dataset_path = sys.argv[1]
except IndexError:
    CVAR_dataset_path = ""
    print('You should enter the absolute path to CVAR dataset!')
    sys.exit(1)

#run the OpenARK to get the fingertip annotations
#os.system("C:\\OpenARK\\x64\\Release\\OpenARK-SDK.exe")

for f in openark_files:
    os.remove(f)

#if os.path.exists('fingertips_openark.txt'):
#    openark_file = open("fingertips_openark.txt")
with open("fingertips_openark.txt") as openark_file:
    #openark_file_lines = openark_file.readlines()
    for line in openark_file:
        line_split = line.split(' ')
        CVAR_depth_image = line_split[0]
        list_of_list = []
        iterable = iter(line_split[1:len(line_split)-1])
        cvar_sliced = list(iter(lambda: list(itertools.islice(iterable, 3)), []))
        cvar_sliced_reverse = cvar_sliced[::-1]
        line_split = ' '.join(line.split(' ')[:]).rstrip()
        line_split = line_split.split(' ')

        CVAR_dir = os.path.dirname(CVAR_depth_image)
        for subdirs, dirs, files in os.walk(CVAR_dataset_path):
            for dir in dirs:
                per_folder_correct_fingertips_count[dir] = 0
                per_folder_accuracy[dir] = 0
                root_path = CVAR_dataset_path + "\\" + dir
                if (os.path.dirname(root_path+"\\") == CVAR_dir):
                    with open("CVAR_folders\\openark_"+os.path.basename(os.path.normpath(CVAR_dir))+".txt", 'a') as openark_tmp_handle:
                        openark_tmp_handle.write(line)

#creating the fingertips.txt file using the given joints.txt file
#joint file includes 21 joints 5 of which belongs to fingertips
for subdirs, dirs, files in os.walk(CVAR_dataset_path):
    for dir in dirs:
        cvar_fingertips_count = 0
        root_path = CVAR_dataset_path+"\\"+dir
        #ex: C:\OpenARK_test\CVAR\P1\all_fingertips.txt
        cvar_fingertips_file_lines = sum(1 for line in open(root_path+"\\"+"all_fingertips.txt"))
        #ex. CVAR_folders\openark_P1.txt
        if os.path.exists("CVAR_folders\\openark_"+dir+".txt"):
            with open("CVAR_folders\\openark_"+dir+".txt", 'r') as openark_cvar_handle:
                openark_line_count = 0
                for line in openark_cvar_handle:
                        openark_line_count += 1
                        line_split = line.split(' ')
                        line_split = ' '.join(line.split(' ')[:]).rstrip()
                        line_split = line_split.split(' ')
                        CVAR_depth_image = line_split[0]
                        CVAR_dir = os.path.dirname(CVAR_depth_image)
                        try:
                            cvar_line = linecache.getline(root_path+"\\"+"all_fingertips.txt", int(os.path.basename(CVAR_depth_image)[:6])+1)
                            cvar_line_split= cvar_line.split(' ')
                            cvar_depth_image = cvar_line_split[0]
                            cvar_line_split = ' '.join(cvar_line_split[1:]).rstrip()
                            cvar_line_split = cvar_line_split.split(' ')
                            iterable = iter(cvar_line_split)
                            cvar_sliced = list(iter(lambda: list(itertools.islice(iterable, 2)), []))
                            cvar_sliced_reversed = cvar_sliced[::-1]
                            line_split = line_split [1:]
                            list_of_list = []
                            iterable = iter(line_split)
                            openark_sliced = list(iter(lambda: list(itertools.islice(iterable, 3)), []))
                            cvar_flag_line = linecache.getline(root_path+"\\"+"visible_fingertips.txt", openark_line_count)
                            cvar_flag_line_split = cvar_flag_line.split(' ')
                            cvar_flag_line_image = cvar_flag_line_split[0]
                            cvar_flag_line_split = ' '.join(cvar_flag_line_split[1:]).rstrip()
                            cvar_flag_line_split = cvar_flag_line_split.split(' ')
                            cvar_flag_reversed = cvar_flag_line_split[::-1]
                            for i in range(len(cvar_flag_reversed)):
                                cvar_fingertips_count += int(cvar_flag_reversed[i])
                            for i in range(len(openark_sliced)):
                                for j in range(len(cvar_sliced_reversed)):
                                    if int(cvar_flag_reversed[j]) == 1:
                                        if (abs(math.sqrt(pow((float(cvar_sliced_reversed[j][0]) - float(openark_sliced[i][0])), 2)
                                            + pow((float(cvar_sliced_reversed[j][1]) - float(openark_sliced[i][1])),2))) < 10):
                                            per_folder_correct_fingertips_count[dir] += 1
                                            total_correct_fingertips_count += 1
                                            break
                        except ValueError:
                            pass

                per_folder_accuracy[dir]= (per_folder_correct_fingertips_count[dir] / cvar_fingertips_count) * 100
                total_CVAR_fingertips += cvar_fingertips_count

print("total fingertips: {0}, total correct fingertips: {1}".format(total_CVAR_fingertips, total_correct_fingertips_count))
accuracy = (total_correct_fingertips_count/total_CVAR_fingertips) *100
print("total accuracy is: {}".format(accuracy))
folder = glob.glob("E:\\datasets\\hand\\CVAR\\test\\*")
print('per folder fingertips count is: \n {}'.format(per_folder_correct_fingertips_count))
print('per folder accuracy is: \n {}'.format(per_folder_accuracy))

