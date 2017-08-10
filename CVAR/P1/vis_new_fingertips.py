import cv2
import itertools
import math
import os

def select_point(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print("x is {0} and y is {1}".format(x,y))
        points.append((x,y))

count = 0
visible_fingertips_file = open('visible_fingertips.txt', 'w+')

#os.remove('correct_fingertips.txt')
#os.remove("all_fingertips.txt")
correct_fingertips_file = open('correct_fingertips.txt', 'a+')
#all_fingertips_file = open('all_fingertips.txt', 'a+')
#correct_fingertips_file.flush()
#os.fsync(correct_fingertips_file.fileno())

with open('all_fingertips.txt') as fingertips_file:
    for line in fingertips_file:
        points = []
        #depth_image_filename = str(count).rjust(6, '0')+'_depth.png'
        fingertips_split = line.split(' ')
        depth_image_filename = fingertips_split[0]
        print(depth_image_filename)
        correct_fingertips_file.write(depth_image_filename+' ')

        visible_fingertips_file.write(depth_image_filename+' ')
        test_image = cv2.imread(depth_image_filename)
        modified_image = test_image.copy()
        modified_image_name = depth_image_filename[:-4]+'_corrected.png'
        line_split = ' '.join(fingertips_split[1:]).rstrip()
        #line_split = ' '.join(line.split(' ')).rstrip()
        line_split = line_split.split(' ')
        iterable = iter(line_split)
        sliced_list = list(iter(lambda: list(itertools.islice(iterable, 2)), []))
        #for item in sliced_list:
            #cv2.circle(test_image, (int(float(item[0])), int(float(item[1]))), 1, (0,255,0), -1)
        cv2.circle(modified_image, (int(float(sliced_list[0][0])), int(float(sliced_list[0][1]))), 1, (255,255,0), -1)
        cv2.circle(modified_image, (int(float(sliced_list[1][0])), int(float(sliced_list[1][1]))), 1, (0,255,255), -1)
        cv2.circle(modified_image, (int(float(sliced_list[2][0])), int(float(sliced_list[2][1]))), 1, (0,255,0), -1)
        cv2.circle(modified_image, (int(float(sliced_list[3][0])), int(float(sliced_list[3][1]))), 1, (0,0,255), -1)
        cv2.circle(modified_image, (int(float(sliced_list[4][0])), int(float(sliced_list[4][1]))), 1, (255,0,0), -1)
        #cv2.namedWindow(depth_image_filename)
        #cv2.imshow(depth_image_filename, test_image)
        #cv2.setMouseCallback(depth_image_filename, select_point)
        cv2.imwrite(modified_image_name,modified_image)
        #image_resized = cv2.resize(test_image, (640, 480), interpolation=cv2.INTER_AREA)
        #cv2.imshow("resized", image_resized)


visible_fingertips_file.close()
correct_fingertips_file.close()




#image_resized = cv2.resize(test_image, (640, 480), interpolation=cv2.INTER_AREA)
#cv2.imshow("resized", image_resized)
#cv2.waitKey(0)


#cv2.destroyAllWindows()


