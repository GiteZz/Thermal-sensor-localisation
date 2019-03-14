'''
this document contains help functions to process the np array from the DB
into a number of objects which are visualised and of which the centroid is determined
to use this class, all you need is the process function, see below
'''
import cv2
import numpy as np
import matplotlib.image as image
import scipy.ndimage.filters as filter


class Img_processor:
    def __init__(self):
        self.data=None
        self.dim=(24,32)
        self.img=None #BGR
        self.gray=None #range(255)
        self.thresh=None #[0|255]
        self.thresh_method="hist_cap"
        self.erode=10

        self.thresh_methods=["otsu","hist_cap"]

    def __get_img(self):
       self.data= np.reshape(self.data,self.dim).astype(np.uint8)
       self.data = filter.gaussian_filter(self.data, 1).astype(np.uint8)
       image.imsave('temp_img.png', self.data)
       self.img=cv2.imread('temp_img.png')
       self.__resize_img()

    def __resize_img(self,factor=10):
        self.img= cv2.resize(self.img,None,fx=factor,fy=factor)

    def __process_into_binary(self):
        self.gray=cv2.cvtColor(self.img,cv2.COLOR_BGR2GRAY)
        if self.thresh_method is "otsu":
            self.gray=255-self.gray
            ret, self.thresh = cv2.threshold(self.gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            self.thresh=255-self.thresh
            self.thresh = cv2.erode(self.thresh, None, iterations=self.erode)
            print('ret=' + str(ret))

        elif self.thresh_method is "hist_cap":
            hist = np.histogram(self.gray, 50);
            thresh_val = hist[1][-5] # -5 is random chosen #TODO make dynamic?
            ret, self.thresh = cv2.threshold(self.gray, thresh_val, 255, cv2.THRESH_BINARY)
            print('ret=' + str(ret))
        else:
            raise NotImplementedError

        return self.thresh

    def __add_contours_and_centroid(self):
        contours, hierarchy = cv2.findContours(self.thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(self.img, contours, -1, 100, 3) #params: all contours,color,thickness
        print('num of contours=' + str(len(contours)))
        for c in contours:
            print(cv2.contourArea(c))
            # calculate moments for each contour
            M = cv2.moments(c)
            # calculate x,y coordinate of center
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
            else:
                cX, cY = 0, 0
            #print(cX)
            #print(cY)
            cv2.circle(self.img, (cX, cY), 5, (255, 255, 0), -1)

    def process(self,data,thresh_method=None,draw=True):
        '''
        this is the public function which implements the whole process
        :param data: a np array of size 24*32 (dimensions don't matter), containing RAW sensor_data
        :param thresh_method:  allows to reselect a thresh method for the class
        :param draw: only false if you want the thresh image (used for tracking)
        :return:  a np.array with dim 24*32*3 in RGB color space, containing all centroids and contours
        '''

        if thresh_method:
            assert(self.thresh_method in self.thresh_methods)
            self.thresh_method=thresh_method
        assert (np.size(data)==int(self.dim[0]*self.dim[1]))
        self.data=data
        self.__get_img()
        thresh=self.__process_into_binary()
        if not draw:
            return thresh
        self.__add_contours_and_centroid()
        #cv2.imshow('res',self.img)
        return cv2.cvtColor(self.img.copy(),cv2.COLOR_BGR2RGB)
