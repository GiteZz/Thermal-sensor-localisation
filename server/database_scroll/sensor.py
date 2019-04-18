from PyQt5.QtWidgets import QGraphicsScene, QFileDialog, QCheckBox, QLabel, QHBoxLayout
from help_module.csv_helper import load_csv
from help_module.data_model_helper import Measurement, Base, CSV_Measurement
from help_module.img_helper import fast_thermal_image, plt_fig_to_PIL, get_deltas_img, grid_plot, hist_plot
from help_module.time_helper import abs_diff
from localization.processing import ImageProcessor
from datetime import timedelta
import scipy.ndimage.filters as filter
from matplotlib.figure import Figure
import numpy as np
import cv2
from PIL import Image

class Sensor:
    def __init__(self, db_bridge, app):
        self.db_bridge = db_bridge
        self.app = app

        self.layout = None
        self.label = None
        self.checkbox = None

        self.checkbox_callback = None
        self.img_processor = ImageProcessor()

        self.start_time = None
        self.stop_time = None

        self.meas_list = None

    def set_sensor_values(self, sensor_type, sensor_id=None, file_name=None, data=None):
        self.sensor_type = sensor_type
        self.meas_list = data
        self.file_name = file_name
        self.sensor_id = sensor_id

    def checkbox_activate(self):
        self.checkbox_callback(self)

    def create_ui(self, callback):
        self.layout = QHBoxLayout()
        self.label = QLabel(f'{self.sensor_type}: {self.sensor_id if self.sensor_id is not None else self.file_name}')
        self.checkbox = QCheckBox()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.checkbox)

        self.checkbox_callback = callback
        self.checkbox.stateChanged.connect(self.checkbox_activate)

        return self.layout

    def delete_ui(self):
        self.layout.deleteLater()
        self.label.deleteLater()
        self.checkbox.deleteLater()

    def data_loaded(self):
        return self.meas_list is not None

    def reload(self):
        if self.meas_list is not None:
            self.load_data()

    def is_active(self):
        return self.checkbox.isChecked()

    def get_data(self):
        if self.meas_list is None:
            print("WARNING attempting to load data that is not loaded")
        return self.meas_list

    def load_data(self):
        """
        This function takes a source and then looks at its type to find the function to get that data

        :param source: A dict containing all the information to load the data
        :return: list of measurements
        """
        if self.sensor_type == 'csv':
            self.meas_list = load_csv(self.file_name)
        elif self.sensor_type == 'sensor':
            self.meas_list = self.load_sensor()
        else:
            raise Exception('Source type was not recognized')

        self.start_time = self.meas_list[0].timestamp
        self.stop_time = self.meas_list[-1].timestamp

        for index, meas in enumerate(self.meas_list):
            meas.set_or_index(index)
            meas.set_sensor(self)
            meas.convert_to_numpy()


    def load_sensor(self):
        """
        Uses a database query to get measurements from the sensor with id == sensor_id

        :param sensor_id:
        :return:
        """
        param = self.app.get_query_param()
        return self.db_bridge.get_values(self.sensor_id, param)

    def get_default_vis(self, index):
        thermal_data = self.meas_list[index].data
        self.img_processor.set_thermal_data(thermal_data)
        imgs_batch_1 = self.img_processor.get_imgs()
        imgs_batch_1.extend(self.img_processor.get_img_layers())

        return imgs_batch_1

    def get_multi_processing(self, index):
        hist_amount = self.img_processor.get_hist_length()
        start_index = max(0, index - hist_amount)
        prev_frames = [meas.data for meas in self.meas_list[start_index:index]]
        cur_frame = self.meas_list[index].data

        self.img_processor.set_current_frame(cur_frame)
        self.img_processor.set_history(prev_frames)

        return self.img_processor.subtract_history()

    def get_closest_meas(self, time):
        cur_time = timedelta(seconds=time)

        min_diff = float('inf')
        min_index = 0

        for meas, index in enumerate(self.meas_list):
            if abs_diff(meas.timestamp, cur_time) < min_diff:
                min_diff = abs_diff(meas.timestamp, cur_time)
                min_index = index

        return min_index

    def multi_plot(self, thermal_data, blur=False, size=10):
        thermal_data = thermal_data.repeat(size, axis=0)
        thermal_data = thermal_data.repeat(size, axis=1)
        if blur:
            thermal_data = filter.gaussian_filter(thermal_data, 10)


        deltas = get_deltas_img(thermal_data)
        imgs = []
        hists = []
        locs = []

        for x in range(3):
            for y in range(4):
                sub_img = thermal_data[x * size * 8:(x + 1) * size * 8, y * size * 8:(y + 1) * size * 8]

                n_img = fast_thermal_image(sub_img, deltas=deltas, dim=(8 * size, 8 * size), side=False)
                n_hist = hist_plot(sub_img.reshape((-1,1)).ravel())
                imgs.append(n_img)
                hists.append(n_hist)
                locs.append((y, x))

        imgs_offset = []
        locs_offset = []

        for x in range(2):
            for y in range(3):
                sub_img = thermal_data[x * size * 8 + size * 4:(x + 1) * size * 8 + size * 4, y * size * 8 + size * 4:(y + 1) * size * 8 + size * 4]

                n_img = fast_thermal_image(sub_img, deltas=deltas, dim=(size * 8, size * 8), side=False)
                imgs_offset.append(n_img)
                locs_offset.append((y, x))

        plot1 = grid_plot(imgs, locs, 100, 100, 15)
        plot2 = grid_plot(hists, locs, 100, 100, 15)
        plot3 = grid_plot(imgs_offset, locs_offset, 100, 100, 15)

        return [plot1, plot2, plot3]
