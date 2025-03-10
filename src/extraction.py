import cv2
import matplotlib.pyplot as plt
import numpy as np

image = cv2.imread("graph.png")

hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

lower_bound = np.array([0, 0, 0])
upper_bound = np.array([180, 50, 200])

lower_blue = np.array([90, 50, 50])
upper_blue = np.array([130, 255, 255])

mask = cv2.inRange(hsv, lower_bound, upper_bound)
mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

def length(mask):
    y1 = 0
    y2 = 0
    for i in range(mask.shape[0]):
        if mask[i][int(mask.shape[1]/2)] == 255:
            y1 = i
            break

    for i in range(mask.shape[0]-1,0,-1):
        if mask[i][int(mask.shape[1]/2)] == 255:
            y2 = i
            break

    return y2-y1

def find_points(mask_blue, mask):
    disp = []
    force = []
    full_len = length(mask)
    ratio_force = 60/full_len
    ratio_disp = 0.6/1280

    for horizontal_num in range(len(mask_blue)):
        for vertical_num in range(len(mask_blue[horizontal_num])):
            if mask_blue[horizontal_num][vertical_num] == 255:
                force.append((547 - horizontal_num)*ratio_force)
                disp.append((vertical_num - 730)*ratio_disp)

    return disp, force
        
def eliminate(mask_blue):

    for row_num in range(len(mask_blue)):

        for column_num in range(len(mask_blue[row_num])):

            if mask_blue[row_num][column_num] == 255:
                count = row_num + 1
                while mask_blue[count][column_num] == 255:
                    mask_blue[count][column_num] = 0
                    count+=1

    return mask_blue


x, y = find_points(eliminate(mask_blue), mask)
plt.scatter(x,y, s=5)
plt.show()

cv2.imshow("mask", mask_blue)






cv2.waitKey(0)
cv2.destroyAllWindows()
