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
        self.dim = (24, 32)

        self.thermal_data = None
        self.scale_factor = 10

        # These variables need to be reset when new thermal data is added
        self.img = None
        self.thresh_img = None
        self.deltas = None
        self.centroids = None
        self.contours = None

        self.thresh_method = "hist_cap"
        self.erode = 4

        self.sensor_id = None

        self.log_system = logging.getLogger('ImageProcessingLogger')

    class decorators:
        """
        This class is used to add decorators to the functions of the ImageProcessor class, these decorators
        are used to check if the needed variables are valid and if they are not generate that data.
        The check_thermal data throws an exception if no thermal data is present.
        """
        @staticmethod
        def check_img(func):
            def wrapper(self):
                if self.img is None:
                    self._set_img()
                return func(self)

            return wrapper

        @staticmethod
        def check_tresh(func):
            def wrapper(self):
                if self.thresh_img is None:
                    self._set_thresh_img()
                return func(self)

            return wrapper

        @staticmethod
        def check_centroids(func):
            def wrapper(self):
                if self.centroids is None:
                    self._set_centroids()
                return func(self)

            return wrapper

        @staticmethod
        def check_deltas(func):
            def wrapper(self):
                if self.deltas is None:
                    self._set_deltas()
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
        """
        If you want output in the terminal, use this function.
        :return:
        """
        c_handler = logging.StreamHandler()
        self.log_system.addHandler(c_handler)
        self.log_system.setLevel(logging.INFO)

    def set_thermal_data(self, thermal_data):
        """
        This function is the function to input data into the class. The useful output only gets calculated
        when needed.
        :param thermal_data: numpy array with dim 786
        :return:
        """
        self.thermal_data = thermal_data
        self._reset()

    @decorators.check_centroids
    def get_centroids(self):
        """
        Get the location of the hotspots on the thermal data.
        :return:
        """
        return self.centroids

    def save_progress(self):
        """
        This function save all the steps in the processing process as images.
        TODO: complete with additional steps
        :return:
        """
        self._save_img()
        self._save_thresh()

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

    def _reset(self):
        """
        Sets all the needed variables to None in order to show that new thermal data is added and the
        old values are invalid.
        :return:
        """
        self.contours = None
        self.centroids = None
        self.thresh_img = None
        self.img = None
        self.deltas = None

    @decorators.check_thermal_data
    def _set_img(self):
        """
        Creates an image (numpy array is good for opencv) that is needed for further analyzing the image,
        First the image gets scaled because opencv works better when there is a bit more resolution.
        Then a blur is added to smooth out the noise. The numpy array has to be np.uint8 to be valid for opencv.
        :return:
        """
        self.log_system.info("Setting image")

        img = np.reshape(self.thermal_data, (24, 32))
        img = img.repeat(10, axis=0)
        img = img.repeat(10, axis=1)

        self.img = filter.gaussian_filter(img, 15).astype(np.uint8)

    @decorators.check_img
    def _set_deltas(self):
        """
        This funtion is used to set the deltas for the fast_thermal_image functions, these deltas are needed to
        make the colors equal on the different images.
        :return:
        """
        self.deltas = get_deltas_img(self.img)

    @decorators.check_img
    def _set_thresh_img(self):
        """
        This function is used to remove the background from the image, this is done by removing everything
        smaller and equal then the temperature that is used most in the image (histogram max).
        :return:
        """
        self.log_system.info("Setting thresh img")

        hist_amount, hist_temp = np.histogram(self.img)
        max_temp_index = np.argmax(hist_amount)

        thresh = self.img.copy()
        thresh_temp = hist_temp[max_temp_index]

        thresh[thresh <= thresh_temp + 1] = 0
        thresh = cv2.erode(thresh, None, iterations=self.erode)
        self.thresh_img = thresh

    @decorators.check_tresh
    def _set_centroids(self):
        """
        This function calculates the centroids from the thresh image. The thresh_img should be set for the initial
        contours. This function also tries to improve the initial contours be searching smaller contours within the
        bigger contours.
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
    def _save_img(self):
        plot_img = fast_thermal_image(self.img, as_numpy=True, deltas=self.deltas, dim=self.img.shape)
        cv2.imwrite("image.png", cv2.cvtColor(plot_img, cv2.COLOR_RGB2BGR))

    @decorators.check_img
    @decorators.check_deltas
    def _save_thresh(self):
        plot_img = fast_thermal_image(self.thresh_img, as_numpy=True, deltas=self.deltas, dim=self.thresh_img.shape)
        cv2.imwrite("thresh_img.png", cv2.cvtColor(plot_img, cv2.COLOR_RGB2BGR))