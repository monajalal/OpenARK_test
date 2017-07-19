import itertools
import math
#cvar_fingertips = "192.518 124.970 649.675 186.809 106.509 623.522 183.797 92.146 608.936 172.665 92.380 591.674 149.250 114.429 537.439"
#openark_fingertips = "175.702 90.5482 594.876"

#cvar_fingertips = "182.636 118.287 641.118 185.646 105.283 639.895 183.230 98.485 647.869 174.614 100.899 617.509 159.797 112.023 548.181"
#openark_fingertips = "159.313 109.051 527.434 178.644 91.3072 601.644"

#cvar_fingertips = "156.550 126.945 658.908 167.037 109.766 656.122 177.948 101.901 643.947 190.789 99.423 618.389 209.115 109.306 538.039"
#openark_fingertips = "157.754 130.208 639.989 177.945 102.819 644.388 188.867 96.9803 619.43 210.005 108.573 539.149 "
#import subprocess
#subprocess.Popen([r"C:\OpenARK\x64\Release\OpenARK-SDK.exe"])
import os

#os.startfile("C:\\OpenARK\\x64\\Release\\OpenARK-SDK.exe")
#os.system("C:\\OpenARK\\x64\\Release\\OpenARK-SDK.exe")
print("hello")

cvar_file = open("fingertips.txt")
cvar_file_lines = cvar_file.readlines()
num_cvar_fingertips = len(cvar_file_lines)*5
correct_fingertips_count = 0

if os.path.exists('fingertips_openark.txt'):
    openark_file = open("fingertips_openark.txt")
    openark_file_lines = openark_file.readlines()

    for line_count in range(len(cvar_file_lines)):
        line_split = ' '.join(cvar_file_lines[line_count].split(' ')[:]).rstrip()
        line_split = line_split.split(' ')
        list_of_list = []
        iterable = iter(line_split)
        cvar_sliced = list(iter(lambda: list(itertools.islice(iterable, 3)), []))
        cvar_sliced_reverse = cvar_sliced[::-1]
        print(cvar_sliced_reverse)
        line_split = ' '.join(openark_file_lines[line_count].split(' ')[:]).rstrip()
        line_split = line_split.split(' ')
        CVAR_folder = line_split[0]
        print(CVAR_folder)
        print(os.path.dirname(CVAR_folder))
        CVAR_dir = os.path.dirname(CVAR_folder)
        line_split = line_split [1:]
        list_of_list = []
        iterable = iter(line_split)
        openark_sliced = list(iter(lambda: list(itertools.islice(iterable, 3)), []))
        print(openark_sliced)

        for i in range(len(openark_sliced)):
            for j in range(len(cvar_sliced_reverse)):
                if (abs(math.sqrt(pow((float(cvar_sliced_reverse[j][0]) - float(openark_sliced[i][0])),2) + pow((float(cvar_sliced_reverse[j][1]) - float(openark_sliced[i][1])),2)  ))<10):
                    correct_fingertips_count+=1
    print(correct_fingertips_count)

if not os.path.exists('accuracy.txt'):
    accuracy_file = open('accuracy', 'w')
    accuracy = (correct_fingertips_count/num_cvar_fingertips) *100
    accuracy_file.write(str(accuracy))
    accuracy_file.close()






