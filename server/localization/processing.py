import cv2
import numpy as np
import matplotlib.image as image
import scipy.ndimage.filters as filter
import math
import scipy.ndimage.filters as fil
from help_module.img_helper import fast_thermal_image, get_deltas_img
import logging


class ImageProcessor:
    def __init__(self):
        self.data = None
        self.dim = (24, 32)

        self.img = None  # BGR
        self.thresh_img = None  # [0|255]
        self.thermal_data = None
        self.deltas = None

        self.thresh_method = "hist_cap"
        self.erode = 4
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

        self.log_system = logging.getLogger('ImageProcessingLogger')

    class decorators:
        @staticmethod
        def check_img(func):
            def wrapper(self):
                if self.img is None:
                    self.set_img()
                return func(self)

            return wrapper

        @staticmethod
        def check_tresh(func):
            def wrapper(self):
                if self.thresh_img is None:
                    self.set_thresh_img()
                return func(self)

            return wrapper

        @staticmethod
        def check_centroids(func):
            def wrapper(self):
                if self.centroids is None:
                    self.set_centroids()
                return func(self)

            return wrapper

        @staticmethod
        def check_deltas(func):
            def wrapper(self):
                if self.deltas is None:
                    self.set_deltas()
                return func(self)

            return wrapper

    def enable_logging(self):
        c_handler = logging.StreamHandler()
        self.log_system.addHandler(c_handler)
        self.log_system.setLevel(logging.INFO)

    def set_img(self):
        self.log_system.info("Setting image")
        if self.thermal_data is None:
            raise Exception('Processing: thermal_data not set')

        img = np.reshape(self.thermal_data, (24, 32))
        img = img.repeat(10, axis=0)
        img = img.repeat(10, axis=1)

        self.img = filter.gaussian_filter(img, 15).astype(np.uint8)

    def set_thermal_data(self, thermal_data):
        self.thermal_data = thermal_data
        self.reset()

    def reset(self):
        self.contours = None
        self.centroids = None
        self.thresh_img = None
        self.img = None
        self.deltas = None

    def get_centroids(self):
        self.set_centroids()
        return self.centroids

    @decorators.check_img
    def set_deltas(self):
        self.deltas = get_deltas_img(self.img)

    @decorators.check_img
    def set_thresh_img(self):
        self.log_system.info("Setting thresh img")

        hist_amount, hist_temp = np.histogram(self.img)
        max_temp_index = np.argmax(hist_amount)

        thresh = self.img.copy()
        thresh_temp = hist_temp[max_temp_index]

        thresh[thresh <= thresh_temp + 1] = 0
        thresh = cv2.erode(thresh, None, iterations=self.erode)
        self.thresh_img = thresh

    @decorators.check_tresh
    def set_centroids(self):
        self.log_system.info("Setting centroids")

        self.centroids = []

        mod_thresh = self.thresh_img - np.min(self.thresh_img)
        scale_factor = math.floor(255 / np.max(mod_thresh))

        self.contours, hierarchy = cv2.findContours(mod_thresh * scale_factor, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
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

    @decorators.check_centroids
    def plot_centroids(self, rel_pos=True, thermal_img=False):
        '''
        public function which adds current centroids & contours to the current image
        :param rel_pos: determines whether the relative coords are added to the figure
        :return: np array in RGB format
        '''
        # add centroids
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

    def save_progress(self):
        self.save_img()
        self.save_thresh()

    @decorators.check_img
    @decorators.check_deltas
    def save_img(self):
        plot_img = fast_thermal_image(self.img, as_numpy=True, deltas=self.deltas, dim=self.img.shape)
        cv2.imwrite("image.png", cv2.cvtColor(plot_img, cv2.COLOR_RGB2BGR))

    @decorators.check_img
    @decorators.check_deltas
    def save_thresh(self):
        plot_img = fast_thermal_image(self.thresh_img, as_numpy=True, deltas=self.deltas, dim=self.thresh_img.shape)
        cv2.imwrite("thresh_img.png", cv2.cvtColor(plot_img, cv2.COLOR_RGB2BGR))