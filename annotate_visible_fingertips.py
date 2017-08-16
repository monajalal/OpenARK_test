__author__ = 'Mona Jalal'

'''
Uses user's left mouse click to annotate the fingertips
Guide from the original CVAR dataset is shown to user and
user should left click on a point close to the fingertip that is 
visible to her.
'''

import cv2
import itertools
import math
import os
import sys

try:
    CVAR_dataset_path = sys.argv[1]
except IndexError:
    CVAR_dataset_path = ""
    print('You should enter the absolute path to CVAR dataset!')
    sys.exit(1)

def select_point(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print("x is {0} and y is {1}".format(x,y))
        points.append((x,y))


for subdirs, dirs, files in os.walk(CVAR_dataset_path):
    for dir in dirs:
        cur_path = CVAR_dataset_path+'\\'+dir
        count = 0
        visible_fingertips_file = open(cur_path+'\\'+'visible_fingertips.txt', 'w+')
        os.remove(cur_path +'\\'+'correct_fingertips.txt')
        os.remove(cur_path+'\\'+'all_fingertips.txt')
        correct_fingertips_file = open(cur_path + '\\'+'correct_fingertips.txt', 'a+')
        all_fingertips_file = open(cur_path + '\\' + 'all_fingertips.txt', 'a+')

        with open(cur_path + '\\' + 'fingertips.txt') as fingertips_file:
            for line in fingertips_file:
                points = []
                fingertips_split = line.split(' ')
                depth_image_filename = fingertips_split[0]
                print(depth_image_filename)
                correct_fingertips_file.write(depth_image_filename+' ')
                all_fingertips_file.write(depth_image_filename+' ')
                visible_fingertips_file.write(depth_image_filename+' ')
                test_image = cv2.imread(cur_path + '\\' +  depth_image_filename)
                line_split = ' '.join(fingertips_split[1:]).rstrip()
                line_split = line_split.split(' ')
                iterable = iter(line_split)
                sliced_list = list(iter(lambda: list(itertools.islice(iterable, 3)), []))

                cv2.circle(test_image, (int(float(sliced_list[0][0])), int(float(sliced_list[0][1]))), 1, (255,255,0), -1)
                cv2.circle(test_image, (int(float(sliced_list[1][0])), int(float(sliced_list[1][1]))), 1, (0,255,255), -1)
                cv2.circle(test_image, (int(float(sliced_list[2][0])), int(float(sliced_list[2][1]))), 1, (0,255,0), -1)
                cv2.circle(test_image, (int(float(sliced_list[3][0])), int(float(sliced_list[3][1]))), 1, (0,0,255), -1)
                cv2.circle(test_image, (int(float(sliced_list[4][0])), int(float(sliced_list[4][1]))), 1, (255,0,0), -1)
                cv2.namedWindow(depth_image_filename)
                cv2.imshow(depth_image_filename, test_image)
                cv2.setMouseCallback(depth_image_filename, select_point)
                count +=1
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                visible_fingertips = {}

                for i in range(5):
                    visible_fingertips[i] = 0

                for i in range(len(points)):
                    for j in range(len(sliced_list)):
                        if (abs(math.sqrt(pow((float(sliced_list[j][0]) - float(points[i][0])), 2)
                                          + pow((float(sliced_list[j][1]) - float(points[i][1])), 2))) < 10):
                            visible_fingertips[j] = 1
                            sliced_list[j][0] = points[i][0]
                            sliced_list[j][1] = points[i][1]
                            print("i is {0} and it is 1".format(j))
                            break

                for i in range(len(sliced_list)):
                    all_fingertips_file.write(str(sliced_list[i][0])+' '+str(sliced_list[i][1])+' ')

                for value in visible_fingertips.values():
                    visible_fingertips_file.write(str(value)+' ')

                print(points)
                print(visible_fingertips)

                for tuple in points:
                    correct_fingertips_file.write(str(tuple[0])+' '+str(tuple[1])+' ')

                correct_fingertips_file.write('\n')
                visible_fingertips_file.write('\n')
                all_fingertips_file.write('\n')

        visible_fingertips_file.close()
        correct_fingertips_file.close()
        all_fingertips_file.close()



