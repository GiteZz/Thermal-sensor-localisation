import sys
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon, QPixmap, QImage, QTransform
import scipy.ndimage.filters as fil
from PyQt5.QtWidgets import QGraphicsScene, QFileDialog, QCheckBox, QLabel, QHBoxLayout
from PyQt5.QtCore import QDateTime, QSize
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import numpy as np
import json
import operator
import time
from PIL.ImageQt import ImageQt
import math
from datetime import timedelta


from ui_generated import Ui_MainWindow
from help_module.data_model_helper import Measurement, Base, CSV_Measurement
from help_module.time_helper import meas_to_time, clean_diff
from help_module.csv_helper import load_csv, write_csv_list_frames, write_csv_frame
from help_module.img_helper import raw_color_plot, blur_color_plot, hist_plot, processed_color_plot, get_grid_form

from qt_extra_classes import ZoomQGraphicsView


class MyUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = None
        with open('configuration.json', 'r') as f:
            data = json.load(f)

        postgres_user = data['postgres']['username']
        postgres_pass = data['postgres']['password']
        postgres_db = data['postgres']['db_name']
        self.engine = create_engine(f'postgres://{postgres_user}:{postgres_pass}@localhost:5432/{postgres_db}')
        Base.metadata.create_all(bind=self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.episode_index = 0
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

        self.source_checkboxes = {}

        self.episodes = []
        self.episode_sensors = []

        self.vis_methods_name = ['matplotlib color raw', 'matplotlib color blur', 'histogram bluf','mtpltlib RGB processed']
        self.vis_methods = [raw_color_plot, blur_color_plot, hist_plot, processed_color_plot]
        self.vis_cur_meth = []
        self.vis_layouts = []
        self.vis_labels = []
        self.vis_checkboxes = []

        self.update_from_button = False

        self.mode = 'frame'

    def confirmUI(self, ui_widgets):
        print("confirming ui")
        self.ui = ui_widgets
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

        self.ui.timeCheckBox.stateChanged.connect(self.to_time_mode)

        for method_name in self.vis_methods_name:
            n_label = QLabel(method_name)
            n_checkbox = QCheckBox()
            n_layout = QHBoxLayout()

            n_layout.addWidget(n_label)
            n_layout.addWidget(n_checkbox)
            n_checkbox.stateChanged.connect(self.update_vis_methods)

            self.ui.visualizeVLayout.addLayout(n_layout)

            self.vis_checkboxes.append(n_checkbox)
            self.vis_labels.append(n_label)
            self.vis_layouts.append(n_layout)

    def update_vis_methods(self):
        self.vis_cur_meth = []
        for index, widg in enumerate(self.vis_checkboxes):
            if widg.isChecked():
                self.vis_cur_meth.append(self.vis_methods[index])
        self.draw_plot()


    def update_connect_time(self, value):
        print("update connect time to " + str(value))
        self.connect_time = value

    def update_slice_time(self, value):
        print("update slice time to: " + str(value))
        self.slice_time = value

    def one_forward(self):
        if self.mode == 'frame':
            if self.frame_index < len(self.episodes[self.episode_index]) - 1:
                self.frame_index += 1
        else:
            if self.time + self.small_time_jump <= self.max_time:
                self.time += self.small_time_jump
        self.adjust_after_shift()

    def one_backward(self):
        if self.mode == 'frame':
            if self.frame_index >= 1:
                self.frame_index -= 1
        else:
            if self.time - self.small_time_jump >= 0:
                self.time -= self.small_time_jump
        self.adjust_after_shift()

    def more_forward(self):
        if self.mode == 'frame':
            if self.frame_index < len(self.episodes[self.episode_index]) - 1 - self.frame_jump:
                self.frame_index += self.frame_jump
        else:
            if self.time + self.big_time_jump <= self.max_time:
                self.time += self.big_time_jump
        self.adjust_after_shift()

    def more_backward(self):
        if self.mode == 'frame':
            if self.frame_index >= self.frame_jump:
                self.frame_index -= self.frame_jump
        else:
            if self.time - self.big_time_jump > 0:
                self.time -= self.big_time_jump
        self.adjust_after_shift()

    def adjust_after_shift(self):
        if self.mode == 'frame':
            slider_index = self.frame_index
        else:
            slider_index = int(self.time)

        self.update_from_button = True
        self.ui.timeSlider.setValue(slider_index)
        self.draw_plot()


    def move_timeslider(self, value):
        if self.update_from_button:
            self.update_from_button = False
            return

        if self.mode == 'frame':
            self.frame_index = value
        else:
            self.time = value
        self.draw_plot()

    def to_time_mode(self):
        if self.ui.timeCheckBox.isChecked():
            self.mode = 'time'
            self.ui.backwardMoreButton.setText(f'-{self.big_time_jump}s')
            self.ui.backwardOneButton.setText(f'-{self.small_time_jump}s')
            self.ui.forwardOneButton.setText(f'+{self.small_time_jump}s')
            self.ui.forwardMoreButton.setText(f'+{self.big_time_jump}s')
        else:
            self.mode = 'frame'
            self.ui.backwardMoreButton.setText('<<<')
            self.ui.backwardOneButton.setText('<')
            self.ui.forwardOneButton.setText('>')
            self.ui.forwardMoreButton.setText('>>>')

    def load_csv_button(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file',
                                            'c:\\', "CSV files (*.csv)")
        if fname[0] != "":
            self.add_csv(fname[0])

    def add_csv(self, filename):
        n_csv_sources = load_csv(filename, split=True)
        for key in n_csv_sources:
            self.add_source('csv_id', file_name=filename, data=n_csv_sources[key], sensor_id=key)

    def add_source(self, type, sensor_id=None, file_name=None, data=None):
        """
        Creates a source but doesn't load in the data, if type == 'csv' file_name should be specified
        If type == 'sensor' sensor_id should be used

        :param type:
        :param sensor_id:
        :param file_name:
        :return:
        """
        new_layout = QHBoxLayout()
        label = QLabel(f'{type}: {sensor_id if sensor_id is not None else file_name}')
        checkbox = QCheckBox()
        new_layout.addWidget(label)
        new_layout.addWidget(checkbox)

        source_set = {'layout': new_layout, 'label': label, 'data': data, 'type': type, 'sensor_id': sensor_id, 'filename': file_name}
        self.source_checkboxes[checkbox] = source_set

        checkbox.stateChanged.connect(self.sensor_state_changed)

        self.ui.sourcesVLayout.addLayout(new_layout)

    def clear_sources(self, type):
        """
        Clears the UI elements and the list that contain references to sources

        :param type: type of source to be removed
        :return:
        """
        for key, value in self.source_checkboxes.items():
            if value['type'] == type:
                res = dict.pop(key)
                res['label'].deleteLater()
                res['layout'].deleteLater()
                key.deleteLater()

    def load_source(self, source):
        """
        This function takes a source and then looks at its type to find the function to get that data

        :param source: A dict containing all the information to load the data
        :return: list of measurements
        """

        if source['type'] == 'csv':
            return load_csv(source['filename'])
        elif source['type'] == 'sensor':
            return self.load_sensor(source['sensor_id'])
        else:
            raise Exception('Source type was not recognized')

    def load_sensor(self, sensor_id):
        """
        Uses a database query to get measurements from the sensor with id == sensor_id
        TODO Take into account the time limits

        :param sensor_id:
        :return:
        """
        start_time = self.ui.startTimeEdit.dateTime().toPyDateTime()
        stop_time = self.ui.stopTimeEdit.dateTime().toPyDateTime()

        basic_query = self.session.query(Measurement).filter(Measurement.sensor_id == sensor_id)

        if not self.ui.ignoreStartCheckbox.isChecked():
            basic_query = basic_query.filter(Measurement.timestamp > start_time)

        if not self.ui.ignoreStopCheckbox.isChecked():
            basic_query = basic_query.filter(Measurement.timestamp < stop_time)


        sensor_values = basic_query.order_by(Measurement.timestamp.desc()). \
            limit(self.ui.frameAmountSpinbox.value()).all()

        return sensor_values

    def sensor_state_changed(self):
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

        # This sometimes happens when clearing listwidgets
        sender = self.sender()

        source = self.source_checkboxes[sender]

        # Load data if not loaded
        if source['data'] is None:
            source['data'] = self.load_source(source)
            self.source_checkboxes[sender] = source

        # Combine data from different sources and sort for easier plotting
        data = []
        for checkbox, source in self.source_checkboxes.items():
            if checkbox.isChecked():
                data.extend(source['data'])

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
            str_timestamp = str(episode[0].timestamp)
            print(str_timestamp)
            self.ui.timeList.addItem(str_timestamp.split('.')[0])

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
        :param meas:
        :param frame:
        :return:
        """
        text_margin = 10

        qt_imgs = [ImageQt(method(meas.data)) for method in self.vis_cur_meth]
        qt_pix = [QPixmap.fromImage(img) for img in qt_imgs]

        plot_amount = len(qt_pix)
        grid = get_grid_form(plot_amount)
        print(f'Current grid is: {grid}')

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
        # TODO optimize
        cut_off_time = 10

        cur_episode = self.episodes[self.episode_index]
        cur_time = cur_episode[0].timestamp + timedelta(seconds=self.time)
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
            value = cur_episode[next_index]
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

        sensor_ids = self.session.query(Measurement).distinct(Measurement.sensor_id).all()
        id_list = [meas.sensor_id for meas in sensor_ids]
        for id in id_list:
            self.add_source('sensor', id)

    def get_csv_current_episode(self):
        print("clicked")
        if not self.episode_selected:
            print('No episode selected')
            return
        write_csv_list_frames(self.episodes[self.episode_index], self.download_path)

    def get_csv_current_frame(self):
        print("clicked")
        if not self.episode_selected:
            return
        write_csv_frame(self.episodes[self.episode_index][self.frame_index], self.download_path)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MyUI()
    ui = Ui_MainWindow()

    ui.setupUi(MainWindow)
    MainWindow.confirmUI(ui)

    MainWindow.show()
    sys.exit(app.exec_())