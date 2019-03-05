import cv2
import matplotlib.pyplot as plt
import scipy.ndimage.filters as filter
import numpy as np
from help_module.csv_helper import read_data
import matplotlib




num=353

data=read_data('sensor_data_episode_20190221-143435_0.csv',0,502) #manually selected empty frames of this episode
im1=data[num][0].reshape((24,32))
im1_b=filter.gaussian_filter(im1,1).astype(np.uint8)
im_bin= np.where(im1_b>28,1,0).astype(np.uint8)
#work around issue of converting python array to opencv img
matplotlib.image.imsave('name.png', im1_b)
'''
ret,thresh = cv2.threshold(im1_b,28,255,0)
cv2.imshow("Image", im1_b)
cv2.waitKey(0)'''

img=cv2.imread('name.png')
img=cv2.resize(img,None,fx=10,fy=10)
gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
cv2.imshow("Image",gray)
cv2.waitKey(0)
#print(gray)
plt.hist(gray.ravel(),256,[0,256])
plt.show()
ret,thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
#basically this filter will make all 'bright' objects smaller, eliminating noise and improving accuracy
thresh=cv2.erode(thresh,None,iterations=8)

print('ret=' + str(ret))
#IMPORTANT! some versions of opencv have 3 output values for this findContours
contours,hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

cv2.drawContours(img,contours,-1,100,3)
for c in contours[1:]:
    # calculate moments for each contour
    M = cv2.moments(c)
    # calculate x,y coordinate of center
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
    else:
        cX, cY = 0, 0
    print(cX)
    print(cY)
    cv2.circle(img, (cX, cY), 5, 100, -1)
# display the image
cv2.imshow("Image", img)
cv2.waitKey(0)

#TODO
#eliminate the necessity to go over a png file
#TODO
#change the dynamic otsu threshold to keep hottest pixels
#=> hist shows that usually there are 2 background colors which are dominant -> make them one!
#TODO
#plot histogram
#TODO
#integrate in db_viewer