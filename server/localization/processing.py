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

        self.log_system = logging.getLogger('ImageProcessingLogger')

    class decorators:
        @staticmethod
        def check_img(func):
            def wrapper(self):
                if self.img is None:
                    self.__set_img()
                return func(self)

            return wrapper

        @staticmethod
        def check_tresh(func):
            def wrapper(self):
                if self.thresh_img is None:
                    self.__set_thresh_img()
                return func(self)

            return wrapper

        @staticmethod
        def check_centroids(func):
            def wrapper(self):
                if self.centroids is None:
                    self.__set_centroids()
                return func(self)

            return wrapper

        @staticmethod
        def check_deltas(func):
            def wrapper(self):
                if self.deltas is None:
                    self.__set_deltas()
                return func(self)

            return wrapper

        @staticmethod
        def check_thermal_data(func):
            def wrapper(self):
                if self.thermal_data is None:
                    raise Exception('Processing: thermal_data not set')
                return func(self)

            return wrapper

    def enable_logging(self):
        c_handler = logging.StreamHandler()
        self.log_system.addHandler(c_handler)
        self.log_system.setLevel(logging.INFO)

    def set_thermal_data(self, thermal_data):
        self.thermal_data = thermal_data
        self.__reset()

    @decorators.check_centroids
    def get_centroids(self):
        return self.centroids

    def save_progress(self):
        """
        This function save all the steps in the processing process as images.
        TODO: complete with additional steps
        :return:
        """
        self.__save_img()
        self.__save_thresh()

    @decorators.check_centroids
    def plot_centroids(self, rel_pos=True):
        '''
        Function that plots the centroids on a representation of the thermal data (fast_thermal_img)
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

    def __reset(self):
        self.contours = None
        self.centroids = None
        self.thresh_img = None
        self.img = None
        self.deltas = None

    @decorators.check_thermal_data
    def __set_img(self):
        self.log_system.info("Setting image")

        img = np.reshape(self.thermal_data, (24, 32))
        img = img.repeat(10, axis=0)
        img = img.repeat(10, axis=1)

        self.img = filter.gaussian_filter(img, 15).astype(np.uint8)

    @decorators.check_img
    def __set_deltas(self):
        self.deltas = get_deltas_img(self.img)

    @decorators.check_img
    def __set_thresh_img(self):
        self.log_system.info("Setting thresh img")

        hist_amount, hist_temp = np.histogram(self.img)
        max_temp_index = np.argmax(hist_amount)

        thresh = self.img.copy()
        thresh_temp = hist_temp[max_temp_index]

        thresh[thresh <= thresh_temp + 1] = 0
        thresh = cv2.erode(thresh, None, iterations=self.erode)
        self.thresh_img = thresh

    @decorators.check_tresh
    def __set_centroids(self):
        """
        This function calculates the centroids from the thresh image
        :return:
        """
        self.log_system.info("Setting centroids")

        self.centroids = []

        unique_val = np.unique(self.thresh_img)

        # Add biggest contours
        or_contours, hierarchy = cv2.findContours(self.thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contour_hier = [or_contours]
        mod_thresh = self.thresh_img.copy()

        # Add contours within other contours
        for i in range(1, unique_val.size - 1):
            mod_thresh[mod_thresh == unique_val[i]] = 0
            con, _ = cv2.findContours(mod_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            contour_hier.append(con)

        self.contours = []
        self.contours.extend(contour_hier[-1])

        # Remove all contours that surround other contours
        for i in reversed(range(0, len(contour_hier) - 1)):
            for new_contour in contour_hier[i]:
                add_contour = True
                for current_contour in self.contours:
                    dst = cv2.pointPolygonTest(new_contour, (current_contour[0, 0, 0], current_contour[0, 0, 1]), True)
                    if dst >= 0:
                        add_contour = False

                if add_contour:
                    self.contours.append(new_contour)

        # Calculate x, y coordinate of contour center
        for c in self.contours:
            M = cv2.moments(c)

            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
            else:
                cX, cY = 0, 0

            self.centroids.append([cX, cY])

    @decorators.check_img
    @decorators.check_deltas
    def __save_img(self):
        plot_img = fast_thermal_image(self.img, as_numpy=True, deltas=self.deltas, dim=self.img.shape)
        cv2.imwrite("image.png", cv2.cvtColor(plot_img, cv2.COLOR_RGB2BGR))

    @decorators.check_img
    @decorators.check_deltas
    def __save_thresh(self):
        plot_img = fast_thermal_image(self.thresh_img, as_numpy=True, deltas=self.deltas, dim=self.thresh_img.shape)
        cv2.imwrite("thresh_img.png", cv2.cvtColor(plot_img, cv2.COLOR_RGB2BGR))