import pyautogui
import time
import cv2
import csv
import numpy as np
import math
import matplotlib.image as im
import matplotlib.pyplot as plt
wait=1
positions=[]

pyautogui.FAILSAFE = True #left top corner detection
xu=0
yu=0
#open layout
img= cv2.imread("layout.png")
cv2.imshow('layout',img)
cv2.waitKey(0) #required for opencv rendering
res=pyautogui.locateOnScreen('plot_edge.png')
if res==None:
    print("detection failed")
else:
    xu,yu,xl,yl=res
    print(xu)
    print(yu)
    time.sleep(1)


try:
    while True:
        res = pyautogui.locateOnScreen('plot_edge.png')
        if res == None:
            print("detection failed")
        else:
            xu, yu, xl, yl = res

        pos= pyautogui.position();
        positions.append([pos.x-xu,pos.y-yu])
        print(positions[-1])
        cv2.circle(img, (positions[-1][0], positions[-1][1]), 5, (0, 0, 255), -1)
        if (len(positions)>=2):
            cv2.line(img, (positions[-2][0], positions[-2][1]), (positions[-1][0], positions[-1][1]), (0, 0, 255), 2)
        cv2.destroyAllWindows()
        cv2.imshow('layout', img)
        cv2.waitKey(0)  # required for opencv rendering
except KeyboardInterrupt:
    print("point capturing terminated")

#TODO: add timestamps
#TODO: gaussion noise on trail
#TODO: divide long lines in subpoints

filename='test'
vel= 110 #cm/s velocity
cv2.imwrite(filename+'.png',img)

with open(filename+'.csv', 'w', newline='') as outfile:
    writer = csv.writer(outfile, delimiter=',')
    writer.writerow(["x_coord","y_coord","rel_time"])
    time=0
    p=np.array(positions)
    p_x=p[:,0]
    p_y=p[:,1]
    d_x=np.ediff1d(p_x)
    d_y=np.ediff1d(p_y)
    d=np.sqrt(np.power(d_x,2)+np.power(d_y,2))
    writer.writerow([positions[0][0],positions[0][1],0])
    for i in range(1,len(positions)):
        writer.writerow([positions[i][0], positions[i][1], d[i-1]/vel])