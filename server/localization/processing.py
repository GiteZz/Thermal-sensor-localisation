import cv2
import numpy as np
import matplotlib.image as image
import scipy.ndimage.filters as filter
import math
import scipy.ndimage.filters as fil
from help_module.img_helper import fast_thermal_image


class ImageProcessor:
    def __init__(self):
        self.data = None
        self.dim = (24, 32)
        self.img = None  # BGR
        self.thresh_img = None  # [0|255]
        self.thresh_method = "hist_cap"
        self.erode = 10
        self.scale_factor = 10
        self.thresh_methods = ["otsu", "hist_cap"]

        self.centroids = []  # 2D array
        self.contours = []

        self.history_amount = 2
        self.past_frames = []
        self.current_frame = None

        self.sensor_id = None

        # Should be smaller then 1/history_amount
        self.weight_min = 1 / 20

    def set_img(self):
        if self.thermal_data is None:
            raise Exception('Processing: thermal_data not set')

        img = np.reshape(self.thermal_data, (24, 32))
        img = img.repeat(10, axis=0)
        img = img.repeat(10, axis=1)

        self.img = filter.gaussian_filter(img, 15).astype(np.uint8)

    def cap_img(self, img):
        hist_amount, hist_temp = np.histogram(img)
        max_temp_index = np.argmax(hist_amount)
        img_ret = img.copy()
        img_ret[img <= hist_temp[max_temp_index]] = 0

        return img_ret

    def set_thermal_data(self, thermal_data):
        self.thermal_data = thermal_data
        self.contours = None
        self.centroids = None
        self.thresh_img = None
        self.img = None

    def get_centroids(self):
        self.set_centroids()
        return self.centroids

    def set_thresh_img(self):
        if self.img is None:
            self.set_img()
        hist_amount, hist_temp = np.histogram(self.img)
        print(hist_amount)
        max_temp_index = np.argmax(hist_amount)
        thresh = self.img.copy()
        thresh[thresh <= hist_temp[max_temp_index]] = 0
        hist_amount, hist_temp = np.histogram(thresh)
        cv2.imshow('im', cv2.cvtColor(fast_thermal_image(thresh, as_numpy=True, dim=self.img.shape), cv2.COLOR_RGB2BGR))
        cv2.waitKey(0)
        thresh = cv2.erode(thresh, None, iterations=self.erode)

        self.thresh_img = thresh

    def set_centroids(self):
        # clear old centroids
        if self.thresh_img is None:
            self.set_thresh_img()
        self.centroids = []
        self.contours, hierarchy = cv2.findContours(self.thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # print('num of contours=' + str(len(self.contours)))
        for c in self.contours:
            M = cv2.moments(c)
            # calculate x,y coordinate of center
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
            else:
                cX, cY = 0, 0
            # print(f'found centroid: {cX}, {cY}')
            self.centroids.append([cX, cY])

    def plot_centroids(self, rel_pos=True, thermal_img=False):
        '''
        public function which adds current centroids & contours to the current image
        :param rel_pos: determines whether the relative coords are added to the figure
        :return: np array in RGB format
        '''
        # add centroids
        if self.centroids is None:
            self.set_centroids()

        draw_img = cv2.cvtColor(fast_thermal_image(self.img, as_numpy=True, dim=self.img.shape), cv2.COLOR_RGB2BGR)

        for centroid in self.centroids:
            [cX, cY] = centroid
            cv2.circle(draw_img, (cX, cY), 5, (255, 255, 0), -1)
            if rel_pos:
                string = str(cX) + "," + str(cY)
                if cX > self.scale_factor * 32 / 2:
                    pos_x = min(cX - len(string) * 10, 32 * self.scale_factor - 15 * (len(string)))
                else:
                    pos_x = cX + 20
                if cY > self.scale_factor * 24 / 2:
                    pos_y = cY - 10
                else:
                    pos_y = cY + 30
                cv2.putText(draw_img, string, (pos_x, pos_y), cv2.QT_FONT_NORMAL, 0.8, (255, 255, 255))
        # add contours
        result = cv2.drawContours(draw_img, self.contours, -1, 100, 3)  # params: all contours,color,thickness
        return result
