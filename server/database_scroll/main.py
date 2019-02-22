import sys
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon, QPixmap, QImage
import scipy.ndimage.filters as fil
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import numpy as np

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

        self.widgets.timeSlider.valueChanged.connect(self.move_timeslider)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.widgets.rightVLayout.insertWidget(0,self.canvas)
        self.ax0 = self.figure.add_subplot(1,2,1)
        self.ax1 = self.figure.add_subplot(1,2,2)

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
        sensor = int(self.widgets.sensorList.item(index).text())
        sensor_values = self.session.query(Measurement).filter(Measurement.sensor_id == sensor). \
            order_by(Measurement.timestamp.desc()).limit(1000).all()

        self.list_episodes = []
        current_starttime = sensor_values[0].timestamp
        current_episode = []
        for value in sensor_values:
            diff = (current_starttime - value.timestamp).seconds
            if diff < 60:
                current_episode.append(value)
            else:
                self.list_episodes.append(current_episode[::-1])
                current_episode = []
            current_starttime = value.timestamp

        if len(current_episode) > 0:
            self.list_episodes.append(current_episode[::-1])

        for episode in self.list_episodes:
            self.widgets.timeList.addItem(str(episode[0].timestamp).split('.')[0])

        print(f'Found {len(self.list_episodes)} different episodes')


    def episode_clicked(self, index):
        self.episode_index = index
        self.widgets.timeSlider.setMinimum(0)
        self.widgets.timeSlider.setMaximum(len(self.list_episodes[self.episode_index]) - 1)
        self.draw_plot()



    def draw_plot(self):
        img_ar = np.transpose(np.array(self.list_episodes[self.episode_index][self.time_index].data).reshape((32,24)))
        result = fil.gaussian_filter(img_ar, 1)

        c = self.ax0.pcolor(img_ar)
        # self.ax0.colorbar(c, ax=self.ax0)
        # plt.gca().set_aspect('equal', adjustable='box')
        d = self.ax1.pcolor(result)
        # self.ax1.colorbar(c, ax=self.ax1)
        # plt.gca().set_aspect('equal', adjustable='box')
        self.ax1.axis('equal')
        self.ax0.axis('equal')

        self.canvas.draw()

    def get_data_db(self):
        sensor_ids = self.session.query(Measurement).distinct(Measurement.sensor_id).all()
        id_list = [meas.sensor_id for meas in sensor_ids]
        for id in id_list:
            self.widgets.sensorList.addItem(str(id))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MyUI()
    ui = Ui_MainWindow()

    ui.setupUi(MainWindow)
    MainWindow.confirmUI(ui)

    MainWindow.show()
    sys.exit(app.exec_())