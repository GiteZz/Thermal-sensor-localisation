import sys
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon, QPixmap, QImage
import scipy.ndimage.filters as fil
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import numpy as np
import csv

from ui_generated import Ui_MainWindow
from db_model import Measurement, Base

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MyUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.widgets = None
        self.engine = create_engine('postgres://postgres:Gilles@localhost:5432/VOP')
        Base.metadata.create_all(bind=self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.episode_index = 0
        self.time_index = 0
        self.more_jump = 4
        self.download_path=''
        self.sensor= 0
        self.episode_selected=0

    def confirmUI(self, ui_widgets):
        print("confirming ui")
        self.widgets = ui_widgets
        self.widgets.refreshButton.clicked.connect(self.get_data_db)
        self.widgets.sensorList.currentRowChanged.connect(self.sensor_clicked)
        self.widgets.timeList.currentRowChanged.connect(self.episode_clicked)

        self.widgets.forwardOneButton.clicked.connect(self.one_forward)
        self.widgets.backwardOneButton.clicked.connect(self.one_backward)
        self.widgets.forwardMoreButton.clicked.connect(self.more_forward)
        self.widgets.backwardMoreButton.clicked.connect(self.more_backward)

        self.widgets.connectTimeSpinbox.valueChanged.connect(self.update_connect_time)
        self.widgets.sliceTimeSpinbox.valueChanged.connect(self.update_slice_time)

        self.widgets.timeSlider.valueChanged.connect(self.move_timeslider)

        self.widgets.saveCSVFRAMEButton.clicked.connect(self.get_csv_current_frame)
        self.widgets.saveCSVEPISODEButton.clicked.connect(self.get_csv_current_episode)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.widgets.rightVLayout.insertWidget(0,self.canvas)
        self.ax0 = self.figure.add_subplot(2,2,1)
        self.ax1 = self.figure.add_subplot(2,2,2)
        self.ax2 = self.figure.add_subplot(2,2,3)

        self.bar1 = None
        self.bar2 = None

        self.connect_time = self.widgets.connectTimeSpinbox.value()
        self.slice_time = self.widgets.sliceTimeSpinbox.value()

    def update_connect_time(self, value):
        print("update connect time to " + str(value))
        self.connect_time = value

    def update_slice_time(self, value):
        print("update slice time to: " + str(value))
        self.slice_time = value

    def one_forward(self):
        if self.time_index < len(self.list_episodes[self.episode_index]) - 1:
            self.widgets.timeSlider.setValue(self.time_index + 1)

    def one_backward(self):
        if self.time_index >= 1:
            self.widgets.timeSlider.setValue(self.time_index - 1)

    def more_forward(self):
        if self.time_index < len(self.list_episodes[self.episode_index]) - 1 - self.more_jump:
            self.widgets.timeSlider.setValue(self.time_index + self.more_jump)

    def more_backward(self):
        if self.time_index >= self.more_jump:
            self.widgets.timeSlider.setValue(self.time_index + self.more_jump)

    def move_timeslider(self, value):
        self.time_index = value
        self.draw_plot()

    def sensor_clicked(self, index):
        print('clicked!  => ' + str(index))
        if index < 0:
            return

        # start_time = self.widgets.startTimeEdit.dateTime().toString('dd.MM.yyyy hh:mm:ss')
        # stop_time = self.widgets.stopTimeEdit.dateTime().toString('dd.MM.yyyy hh:mm:ss')
        # filter(Measurement.timestamp <= stop_time).filter(Measurement.timestamp >= start_time). \

        sensor = int(self.widgets.sensorList.item(index).text())
        sensor_values = self.session.query(Measurement).filter(Measurement.sensor_id == sensor). \
            order_by(Measurement.timestamp.desc()).limit(1000).all()

        self.list_episodes = []
        episode_starttime = sensor_values[0].timestamp
        current_starttime = sensor_values[0].timestamp
        current_episode = []

        for value in sensor_values:
            if len(current_episode) == 0:
                episode_starttime = value.timestamp

            diff_connect = (current_starttime - value.timestamp).seconds
            diff_slice = (episode_starttime - value.timestamp).seconds
            if (diff_connect < self.connect_time or self.connect_time == 0) and (diff_slice < self.slice_time or self.slice_time == 0):
                current_episode.append(value)
            else:
                if len(current_episode) > 0:
                    self.list_episodes.append(current_episode[::-1])
                current_episode = []
            current_starttime = value.timestamp

        if len(current_episode) > 0:
            self.list_episodes.append(current_episode[::-1])

        for episode in self.list_episodes:
            str_timestamp = str(episode[0].timestamp)
            print(str_timestamp)
            self.widgets.timeList.addItem(str_timestamp.split('.')[0])

        print(f'Found {len(self.list_episodes)} different episodes')

    def episode_clicked(self, index):
        self.episode_index = index
        self.time_index = 0
        self.widgets.frameAmountLabel.setText(f'frame: 1/{len(self.list_episodes[self.episode_index])}')
        self.widgets.startEpisodeLabel.setText(f'Start: {self.meas_to_time(self.list_episodes[self.episode_index][0])}')
        self.widgets.endEpisodeLabel.setText(f'Stop: {self.meas_to_time(self.list_episodes[self.episode_index][-1])}')
        self.widgets.timeSlider.setMinimum(0)
        self.widgets.timeSlider.setMaximum(len(self.list_episodes[self.episode_index]) - 1)
        self.draw_plot()
        self.episode_seleced=1

    def draw_plot(self):
        current_meas = self.list_episodes[self.episode_index][self.time_index]
        img_ar = np.array(current_meas.data).reshape((24,32))
        result = fil.gaussian_filter(img_ar, 1)

        min_frame = np.min(result)
        max_frame = np.max(result)
        av_frame = np.average(result)

        self.widgets.minLabel.setText(f'min: {min_frame}')
        self.widgets.maxLabel.setText(f'max: {max_frame}')
        self.widgets.avLabel.setText(f'av: {round(av_frame,1)}')
        self.widgets.frameAmountLabel.setText(f'frame: {self.time_index + 1}/{len(self.list_episodes[self.episode_index])}')
        self.widgets.frameTimeLabel.setText(f'Frame time: {self.meas_to_time(current_meas)}')

        c = self.ax0.pcolor(img_ar)
        if self.bar1 is None:
            self.bar1 = self.figure.colorbar(c, ax=self.ax0)
        else:
            self.bar1.update_bruteforce(c)

        d = self.ax1.pcolor(result)
        if self.bar2 is None:
            self.bar2 = self.figure.colorbar(d, ax=self.ax1)
        else:
            self.bar2.update_bruteforce(d)

        self.ax2.clear()
        self.ax2.hist(current_meas.data, bins=20)

        self.ax1.axis('equal')
        self.ax0.axis('equal')

        self.canvas.draw()

    def get_data_db(self):
        self.widgets.sensorList.clear()
        self.widgets.timeList.clear()

        sensor_ids = self.session.query(Measurement).distinct(Measurement.sensor_id).all()
        id_list = [meas.sensor_id for meas in sensor_ids]
        for id in id_list:
            self.widgets.sensorList.addItem(str(id))

    def get_csv_current_episode(self):
        if not self.episode_selected:
            return
        frame = self.list_episodes[self.episode_index][0]
        frame_time = frame.timestamp
        frame_time_arr = (str(frame_time)).replace('-', ',').replace('.', ',').replace(' ', ',').replace(':',',').split(',')
        time = frame_time_arr[0] + frame_time_arr[1] + frame_time_arr[2] + '-' + frame_time_arr[3] + frame_time_arr[4] + frame_time_arr[5]
        filename = self.download_path + 'sensor_data_episode' + '_' + time + '_' + str(self.sensor) + '.csv'
        print('filename=' + filename)
        with open(filename, 'w') as outfile:
            writer = csv.writer(outfile, delimiter=',')
            writer.writerow(['data', 'timestamp', 'sequence_ID', 'sensor_ID', 'data_type'])
            for frame in self.list_episodes[self.episode_index]:
                writer.writerow([frame.data, frame.timestamp, frame.sequence_id, frame.sensor_id, frame.data_type])
        print('csv saved')

    def get_csv_current_frame(self):

        if not self.episode_selected:
            return
        frame=self.list_episodes[self.episode_index][self.time_index]
        frame_time = frame.timestamp
        frame_time_arr=(str(frame_time)).replace('-',',').replace('.',',').replace(' ',',').replace(':',',').split(',')
        time=frame_time_arr[0]+frame_time_arr[1]+frame_time_arr[2]+'-'+frame_time_arr[3]+frame_time_arr[4]+frame_time_arr[5]
        filename= self.download_path+'sensor_data_frame'+'_'+time+'_'+str(self.sensor)+'.csv'
        print('filename='+filename)
        with open (filename,'w') as outfile:
            writer=csv.writer(outfile, delimiter=',')
            writer.writerow(['data','timestamp','sequence_ID','sensor_ID','data_type'])
            writer.writerow([frame.data,frame.timestamp,frame.sequence_id,frame.sensor_id,frame.data_type])
        print('csv saved')

    def meas_to_time(self, meas):
        return str(meas.timestamp).split(".")[0]


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MyUI()
    ui = Ui_MainWindow()

    ui.setupUi(MainWindow)
    MainWindow.confirmUI(ui)

    MainWindow.show()
    sys.exit(app.exec_())