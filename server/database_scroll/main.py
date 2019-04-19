import sys
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon, QPixmap, QImage, QTransform
import scipy.ndimage.filters as fil
from PyQt5.QtWidgets import QGraphicsScene, QFileDialog, QCheckBox, QLabel, QHBoxLayout
from PyQt5.QtCore import QDateTime, QSize

import numpy as np
import json
import operator
import time
from PIL.ImageQt import ImageQt
import math
from datetime import timedelta


from server.database_scroll.ui_generated import Ui_MainWindow
from help_module.data_model_helper import Measurement, Base, CSV_Measurement
from help_module.time_helper import meas_to_time, clean_diff, get_time_str
from help_module.csv_helper import load_csv, write_csv_list_frames, write_csv_frame
from help_module.img_helper import get_grid_form


from server.database_scroll.qt_extra_classes import ZoomQGraphicsView
from server.database_scroll.db_bridge import DB_Bridge
from server.database_scroll.sensor import Sensor
import logging


class MyUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.episode_index = -1
        self.frame_index = 0
        self.frame_jump = 10
        self.time = 0
        self.time_to_index = 0
        self.max_time = 0
        self.small_time_jump = 0.25
        self.big_time_jump = 1
        self.download_path = ''
        self.sensor = 0
        self.episode_selected = 0

        self.episodes = []
        self.episode_sensors = []

        self.update_from_button = False

        self.mode = 'frame'

        self.ui.refreshButton.clicked.connect(self.refresh_sensor_ids)
        self.ui.timeList.currentRowChanged.connect(self.episode_clicked)

        self.ui.forwardOneButton.clicked.connect(self.one_forward)
        self.ui.backwardOneButton.clicked.connect(self.one_backward)
        self.ui.forwardMoreButton.clicked.connect(self.more_forward)
        self.ui.backwardMoreButton.clicked.connect(self.more_backward)

        self.ui.connectTimeSpinbox.valueChanged.connect(self.update_connect_time)
        self.ui.sliceTimeSpinbox.valueChanged.connect(self.update_slice_time)

        self.ui.timeSlider.valueChanged.connect(self.move_timeslider)

        self.ui.saveCSVFRAMEButton.clicked.connect(self.get_csv_current_frame)
        self.ui.saveCSVEPISODEButton.clicked.connect(self.get_csv_current_episode)
        self.ui.loadCSVButton.clicked.connect(self.load_csv_button)

        now = QDateTime()
        now.setSecsSinceEpoch(time.time())

        yesterday = QDateTime()
        yesterday.setSecsSinceEpoch(time.time() - 24*60*60)

        self.ui.startTimeEdit.setDateTime(yesterday)
        self.ui.stopTimeEdit.setDateTime(now)

        self.connect_time = self.ui.connectTimeSpinbox.value()
        self.slice_time = self.ui.sliceTimeSpinbox.value()

        self.plotGraphicsView = ZoomQGraphicsView()

        self.ui.rightVLayout.insertWidget(0, self.plotGraphicsView)
        self.plot_scene = QGraphicsScene()
        self.plotGraphicsView.setScene(self.plot_scene)

        self.ui.frameAmountSpinbox.valueChanged.connect(self.update_episodes_ui_update)
        self.ui.sliceTimeSpinbox.valueChanged.connect(self.update_episodes_ui_update)
        self.ui.connectTimeSpinbox.valueChanged.connect(self.update_episodes_ui_update)
        self.ui.stopTimeEdit.dateTimeChanged.connect(self.update_episodes_ui_update)
        self.ui.startTimeEdit.dateTimeChanged.connect(self.update_episodes_ui_update)
        self.ui.ignoreStartCheckbox.stateChanged.connect(self.update_episodes_ui_update)
        self.ui.ignoreStopCheckbox.stateChanged.connect(self.update_episodes_ui_update)

        self.sensors = []

        self.or_index_counter = 0
        
        self.logger = logging.getLogger('database_scrol_logger')

        self.db_bridge = DB_Bridge()

    def update_connect_time(self, value):
        self.logger.info("update connect time to " + str(value))
        self.connect_time = value

    def update_slice_time(self, value):
        self.logger.info("update slice time to: " + str(value))
        self.slice_time = value

    def one_forward(self):
        self.move_time_or_frame(self.small_time_jump, 1)

    def one_backward(self):
        self.move_time_or_frame(-self.small_time_jump, -1)

    def more_forward(self):
        self.move_time_or_frame(self.big_time_jump, self.frame_jump)

    def more_backward(self):
        self.move_time_or_frame(-self.big_time_jump, -self.frame_jump)

    def move_time_or_frame(self, time_jump, frame_jump):
        if self.episode_index < 0 or self.episode_index >= len(self.episodes):
            return
        if self.mode == 'frame':
            if 0 <= self.frame_index + frame_jump < len(self.episodes):
                self.frame_index += frame_jump
        else:
            if 0 <= self.time + time_jump <= self.max_time:
                self.time += time_jump
        self.adjust_after_shift()


    def adjust_after_shift(self):
        self.logger.info("Adjust after shift")
        if self.mode == 'frame':
            slider_index = self.frame_index
        else:
            slider_index = int(self.time)

        self.update_from_button = True
        self.ui.timeSlider.setValue(slider_index)
        self.draw_plot()

    def update_episodes_ui_update(self):
        self.reload_sources('sensor')
        self.update_episodes()


    def move_timeslider(self, value):
        if self.update_from_button:
            self.update_from_button = False
            return

        if self.mode == 'frame':
            self.frame_index = value
        else:
            self.time = value
        self.draw_plot()

    def load_csv_button(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file',
                                            'c:\\', "CSV files (*.csv)")
        if fname[0] != "":
            self.add_csv(fname[0])

    def add_csv(self, filename):
        n_csv_sources = load_csv(filename, split=True)
        for key in n_csv_sources:
            self.add_source('csv_id', file_name=filename, data=n_csv_sources[key], sensor_id=key)

    def add_source(self, sensor_type, sensor_id=None, file_name=None, data=None):
        """
        Creates a source but doesn't load in the data, if type == 'csv' file_name should be specified
        If type == 'sensor' sensor_id should be used

        :param sensor_type:
        :param sensor_id:
        :param file_name:
        :return:
        """
        n_sensor = Sensor(self.db_bridge, self)
        n_sensor.set_sensor_values(sensor_type, sensor_id, file_name, data)
        new_layout = n_sensor.create_ui(self.sensor_state_changed)
        self.sensors.append(n_sensor)
        self.ui.sourcesVLayout.addLayout(new_layout)

    def clear_sources(self, sensor_type):
        """
        Clears the UI elements and the list that contain references to sources

        :param type: type of source to be removed
        :return:
        """
        n_list = [sensor for sensor in self.sensors if sensor.sensor_type != sensor_type]
        del_list = [sensor for sensor in self.sensors if sensor.sensor_type == sensor_type]

        for sensor in del_list:
            sensor.delete_ui()

        self.sensors = n_list

    def get_query_param(self):
        """
        This functions creates a dict that is needed to get the correct information from the db.
        This is needed because there is no direct connection with the db only via the db_bridge.
        :return:
        """
        param = {}
        param['act_start'] = not self.ui.ignoreStartCheckbox.isChecked()
        param['act_stop'] = not self.ui.ignoreStopCheckbox.isChecked()
        param['time_start'] = self.ui.startTimeEdit.dateTime().toPyDateTime()
        param['time_stop'] = self.ui.stopTimeEdit.dateTime().toPyDateTime()
        param['amount_limit'] = self.ui.frameAmountSpinbox.value()

        return param

    def reload_sources(self, type):
        for sensor in self.sensors:
            sensor.reload()

    def sensor_state_changed(self, sensor):
        """
        This function looks at the selected sources and then creates a episode list.
        A episode is defined as measurements that all satisfy the conditions.

        cond1: The next measurement should be within self.connect_time from the previous one. This is used
        to separate different bursts of measurements. If zero this is ignored.

        cond2: The difference in time between first and last measurement should be smaller then
        self.slice_time. This is used to avoid excessive long episodes. If zero this is ignored.

        :param index: This gives the index of the current sensor index
        :return: Fills up self.episodes
        """

        # Load data if not loaded
        if not sensor.data_loaded():
            sensor.load_data()

        self.update_episodes()

    def update_episodes(self):
        """
        Calculate episodes based on the selected checkboxes.
        :return:
        """
        # Combine data from different sources and sort for easier plotting
        data = []
        for sensor in self.sensors:
            if sensor.is_active():
                data.extend(sensor.get_data())

        data = sorted(data, key=operator.attrgetter('timestamp'), reverse=True)

        # Clear UI and setup variables
        self.episodes = []
        self.episode_sensors = []
        self.ui.timeList.clear()

        if len(data) == 0:
            return

        episode_starttime = data[0].timestamp
        current_starttime = data[0].timestamp
        current_episode = []
        current_set = {data[0].sensor_id}

        # Slice the data up into episodes
        for value in data:
            if len(current_episode) == 0:
                episode_starttime = value.timestamp

            diff_connect = (current_starttime - value.timestamp).seconds
            diff_slice = (episode_starttime - value.timestamp).seconds
            if (diff_connect < self.connect_time or self.connect_time == 0) and (diff_slice < self.slice_time or self.slice_time == 0):
                current_episode.append(value)
                current_set.add(value.sensor_id)
            else:
                if len(current_episode) > 0:
                    self.episodes.append(current_episode[::-1])
                    self.episode_sensors.append(current_set)
                current_episode = []
                current_set = set()
            current_starttime = value.timestamp

        if len(current_episode) > 0:
            self.episodes.append(current_episode[::-1])
            self.episode_sensors.append(current_set)

        # Create string for UI list and populate that list
        for episode in self.episodes:
            date_str = get_time_str(episode[0].timestamp, time=False)
            start_time_str = get_time_str(episode[0].timestamp, date=False)
            stop_time_str = get_time_str(episode[-1].timestamp, date=False)

            episode_str = f'{date_str} {start_time_str}->{stop_time_str}'
            self.ui.timeList.addItem(episode_str)

    def episode_clicked(self, index):
        """
        This function sets up the UI to handle an episode (mostly plotting stuff)

        :param index: episode clicked on self.timeList
        :return:
        """
        if index < 0:
            self.clear_frame()
            return

        self.episode_index = index
        episode = self.episodes[index]
        self.frame_index = 0
        diff = (episode[-1].timestamp - episode[0].timestamp)
        self.max_time = diff.seconds

        self.ui.frameAmountLabel.setText(f'frame: 1/{len(episode)}')
        self.ui.startEpisodeLabel.setText(f'Start: {meas_to_time(episode[0])}')
        self.ui.endEpisodeLabel.setText(f'Stop: {meas_to_time(episode[-1])}')
        self.ui.sensorEpisodeLabel.setText(f'Sensors: {self.episode_sensors[index]}')
        self.ui.lengthEpisodeLabel.setText(f'Length: 0/{self.max_time}s')
        self.ui.timeSlider.setMinimum(0)
        if self.mode == 'frame':
            self.ui.timeSlider.setMaximum(len(self.episodes[self.episode_index]) - 1)
        else:
            self.ui.timeSlider.setMaximum(int(self.max_time) - 1)
        self.draw_plot()
        self.episode_selected = 1

    def clear_frame(self):
        """
        Clear plots and all the frame/episode stats

        :return:
        """
        self.plot_scene.clear()

        self.ui.frameAmountLabel.setText(f'frame: -/-')
        self.ui.startEpisodeLabel.setText(f'Start: -')
        self.ui.endEpisodeLabel.setText(f'Stop: -')
        self.ui.minLabel.setText(f'min: -')
        self.ui.maxLabel.setText(f'max: -')
        self.ui.avLabel.setText(f'av: -')

        self.ui.frameTimeLabel.setText(f'Frame time: -')

    def draw_plot(self):
        self.plot_scene.clear()

        if self.episode_index < 0:
            return

        scene_size = self.plotGraphicsView.size()

        self.qt_imgs = []
        self.qt_pix = []

        margin = math.floor(0.05 * scene_size.width())
        if margin > 20:
            margin = 20

        frame_width = scene_size.width() - 2 * margin
        frame_height = scene_size.height() - 2 * margin
        frame_x_start = margin
        frame_y_start = margin

        if self.mode == 'frame':
            current_meas = self.episodes[self.episode_index][self.frame_index]
            frame = (frame_x_start, frame_y_start, frame_width, frame_height)
            qt_imgs, qt_pix = self.draw_frame(current_meas, frame)
            self.qt_imgs.extend(qt_imgs)
            self.qt_pix.extend(qt_pix)

            self.ui.frameTimeLabel.setText(f'Frame time: {meas_to_time(current_meas, seconds=True)}')
            self.ui.sensorLabel.setText(f'Sensor: {current_meas.sensor_id}')
        else:
            meas = self.get_close_measurements()
            keys = list(meas.keys())
            keys.sort()

            grid = get_grid_form(len(meas))

            grid_width = math.floor(frame_width / grid[0])
            grid_height = math.floor(frame_height / grid[1])

            for index, key in enumerate(keys):
                value = meas[key]

                offset_x = grid_width * (index % grid[0]) + frame_x_start
                offset_y = grid_height * (index // grid[0]) + frame_y_start

                frame = (offset_x, offset_y, grid_width, grid_height)
                qt_imgs, qt_pix = self.draw_frame(value, frame)
                self.qt_imgs.extend(qt_imgs)
                self.qt_pix.extend(qt_pix)

    def draw_frame(self, meas, frame):
        """
        frame consist of (x0,y0,width, height)
        This draw the given meas in the given frame on the graphicsscene.
        :param meas:
        :param frame:
        :return:
        """
        text_margin = 10

        if meas.sensor == None:
            meas.sensor = self.sensors[0]
        if meas.or_index == None:
            meas.or_index = self.or_index_counter
            self.or_index_counter += 1

        sensor = meas.sensor
        imgs = sensor.get_default_vis(meas.or_index)
        qt_imgs = [ImageQt(img) for img in imgs]
        qt_pix = [QPixmap.fromImage(img) for img in qt_imgs]

        plot_amount = len(qt_pix)
        grid = get_grid_form(plot_amount)
        self.logger.info(f'Current grid is: {grid}')

        frame_width = frame[2]
        frame_height = frame[3] - text_margin
        grid_width = math.floor(frame_width / grid[0])
        grid_height = math.floor(frame_height / grid[1])

        # pix_res = [pix.scaled(grid_size, aspectRatioMode=1) for pix in qt_pix]

        for index, pix in enumerate(qt_pix):
            frame_offset_x = grid_width * (index % grid[0]) + frame[0]
            frame_offset_y = grid_height * (index // grid[0]) + frame[1] + text_margin

            img_size = pix.size()
            img_width = img_size.width()
            img_height = img_size.height()
            scale_x = grid_width / img_width
            scale_y = grid_height / img_height

            scale = scale_x if scale_x < scale_y else scale_y

            scene_img = self.plot_scene.addPixmap(pix)
            scene_img.setScale(scale)

            img_offset_x = (grid_width - img_width * scale) / (2 * scale)
            img_offset_y = (grid_height - img_height * scale) / (2 * scale)

            scene_img.setPos(img_offset_x + frame_offset_x, img_offset_y + frame_offset_y)

        scene_text = self.plot_scene.addText(str(meas.sensor_id))
        scene_text.setPos(frame[0] + 2, frame[1] + 2)

        self.plot_scene.addRect(frame[0], frame[1], frame_width, frame_height)

        return qt_imgs, qt_pix

    def draw_time(self):
        self.plot_scene.clear()

    def get_close_measurements(self):
        """
        This function is used when the program runs in time mode, this searches for measurements for all id's
        that are closest the the given time.
        :return:
        """
        cut_off_time = 10

        cur_episode = self.episodes[self.episode_index]
        cur_time = cur_episode[0].timestamp + timedelta(seconds=self.time)
        self.ui.frameTimeLabel.setText(str(cur_time))
        min_diff = float('inf')
        min_index = -1


        # Find closest meas
        for index, value in enumerate(cur_episode):
            diff = clean_diff(cur_time, value.timestamp)
            if abs(diff) < min_diff:
                min_diff = abs(diff)
                min_index = index
            else:
                break

        diff_set = {}
        meas_set = {}

        next_index = min_index
        while next_index < len(cur_episode):
            value = cur_episode[next_index]
            diff = clean_diff(value.timestamp, cur_time)
            if value.sensor_id not in diff_set:
                diff_set[value.sensor_id] = diff
                meas_set[value.sensor_id] = value

            if diff > cut_off_time:
                break

            next_index += 1

        prev_index = min_index
        while prev_index > 0:
            value = cur_episode[prev_index]
            diff = clean_diff(cur_time, value.timestamp)

            if value.sensor_id in diff_set and diff_set[value.sensor_id] > diff:
                diff_set[value.sensor_id] = diff
                meas_set[value.sensor_id] = value

            if diff > cut_off_time:
                break

            prev_index -= 1

        return meas_set

    def refresh_sensor_ids(self):
        self.clear_sources('sensor')

        id_list = self.db_bridge.get_distinct_ids()
        for id in id_list:
            self.add_source('sensor', id)

    def get_csv_current_episode(self):
        self.logger.info("clicked")
        if not self.episode_selected:
            self.logger.info('No episode selected')
            return
        write_csv_list_frames(self.episodes[self.episode_index], self.download_path)

    def get_csv_current_frame(self):
        self.logger.info("clicked")
        if not self.episode_selected:
            return
        write_csv_frame(self.episodes[self.episode_index][self.frame_index], self.download_path)


app = QtWidgets.QApplication(sys.argv)
MainWindow = MyUI()
MainWindow.show()
sys.exit(app.exec_())