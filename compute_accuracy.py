__author__ = "Mona Jalal"

import itertools
import math
from PIL import Image
import numpy as np
import cv2
import glob
import os
import itertools
import linecache

openark_line_count = 0
total_correct_fingertips_count = 0
total_CVAR_fingertips = 0
per_folder_correct_fingertips_count = {}
per_folder_accuracy = {}
openark_files = glob.glob("CVAR_folders\\*.txt")
CVAR_dataset_path = "C:\\OpenARK_test\\CVAR"
#CVAR_dataset_path = "E:\\datasets\\hand\\CVAR\\test"


'''for subdirs, dirs, files in os.walk(CVAR_dataset_path):
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

os.chdir('C:\\OpenARK_test')

os.system("C:\\OpenARK\\x64\\Release\\OpenARK-SDK.exe")
'''


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
                #ex. CVAR_folders\openark_P1.txt
                fingertips_file = open(root_path + "\\" + "fingertips.txt", 'w')
                if (os.path.dirname(root_path+"\\") == CVAR_dir):
                    with open("CVAR_folders\\openark_"+os.path.basename(os.path.normpath(CVAR_dir))+".txt", 'a') as openark_tmp_handle:
                        openark_tmp_handle.write(line)

#creating the fingertips.txt file using the given joints.txt file
#joint file includes 21 joints 5 of which belongs to fingertips
for subdirs, dirs, files in os.walk(CVAR_dataset_path):
    for dir in dirs:
        root_path = CVAR_dataset_path+"\\"+dir
        #ex: C:\OpenARK_test\CVAR\P1\fingertips.txt
        fingertips_file = open(root_path+"\\"+"fingertips.txt", 'w')
        with open(root_path+"\\"+"joint.txt") as joints_file:
            next(joints_file)
            for line in joints_file:
                #print("line split{0}".format(line_split))
                line_split = ' '.join(line.split(' ')[1:]).rstrip()
                line_split = line_split.split(' ')
                list_of_list = []
                iterable = iter(line_split)
                sliced_list = list(iter(lambda: list(itertools.islice(iterable, 3)), []))
                fingertips = []
                fingertips.extend((sliced_list[16], sliced_list[12], sliced_list[8], sliced_list[4], sliced_list[20]))
                flat_list = [item for sublist in fingertips for item in sublist]
                str_flat_list = " ".join(str(x) for x in flat_list)
                fingertips_file.write(str_flat_list + "\n")
        fingertips_file.close()

        cvar_fingertips_file = open(root_path+"\\"+"fingertips.txt")
        cvar_fingertips_file_lines = cvar_fingertips_file.readlines()
        cvar_fingertips_count = len(cvar_fingertips_file_lines) * 5
        total_CVAR_fingertips += cvar_fingertips_count
        #ex. CVAR_folders\openark_P1.txt
        openark_cvar_handle = open("CVAR_folders\\openark_"+dir+".txt", 'r')
        for line in openark_cvar_handle:
                openark_line_count += 1
                line_split = line.split(' ')
                line_split = ' '.join(line.split(' ')[:]).rstrip()
                line_split = line_split.split(' ')
                CVAR_depth_image = line_split[0]
                CVAR_dir = os.path.dirname(CVAR_depth_image)
                try:
                    cvar_line = linecache.getline(root_path+"\\"+"fingertips.txt", int(os.path.basename(CVAR_depth_image)[:6])+1)
                    cvar_line_split = ' '.join(cvar_line.split(' ')[:]).rstrip()
                    cvar_line_split = cvar_line_split.split(' ')
                    iterable = iter(cvar_line_split)
                    cvar_sliced = list(iter(lambda: list(itertools.islice(iterable, 3)), []))
                    cvar_sliced_reversed = cvar_sliced[::-1]
                    line_split = line_split [1:]
                    list_of_list = []
                    iterable = iter(line_split)
                    openark_sliced = list(iter(lambda: list(itertools.islice(iterable, 3)), []))
                    for i in range(len(openark_sliced)):
                        for j in range(len(cvar_sliced_reversed)):
                            if (abs(math.sqrt(pow((float(cvar_sliced_reversed[j][0]) - float(openark_sliced[i][0])),2)
                                + pow((float(cvar_sliced_reversed[j][1]) - float(openark_sliced[i][1])),2)  ))<10):
                                per_folder_correct_fingertips_count[dir]+=1
                                total_correct_fingertips_count+=1
                except ValueError:
                    pass

        accuracy_file = open(dir+'_accuracy', 'w')
        print("cvar fingertips count is: {}".format(cvar_fingertips_count))
        print(per_folder_correct_fingertips_count)
        print(per_folder_correct_fingertips_count[dir])
        per_finger_accuracy = (per_folder_correct_fingertips_count[dir] / cvar_fingertips_count) * 100
        accuracy_file.write(str(per_finger_accuracy))
        print("per finger accuracy {}".format(per_finger_accuracy))
        accuracy_file.close()

accuracy_file = open('accuracy', 'w')
print("total fingertips: {0}, total correct fingertips {1}".format(total_CVAR_fingertips, total_correct_fingertips_count))
accuracy = (total_correct_fingertips_count/total_CVAR_fingertips) *100
accuracy_file.write(str(accuracy))
print("total accuracy is {}".format(accuracy))
accuracy_file.close()
print("openark line count {}".format(openark_line_count))
folder = glob.glob("E:\\datasets\\hand\\CVAR\\test\\*")
print(len(folder))



