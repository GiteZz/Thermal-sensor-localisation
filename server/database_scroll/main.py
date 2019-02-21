import sys
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon, QPixmap, QImage
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import numpy as np

from ui_generated import Ui_MainWindow
from db_model import Measurement, Base

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

    def confirmUI(self, ui_widgets):
        print("confirming ui")
        self.widgets = ui_widgets
        self.widgets.refreshButton.clicked.connect(self.get_data_db)
        self.widgets.sensorList.currentRowChanged.connect(self.sensor_clicked)
        self.widgets.timeList.currentRowChanged.connect(self.episode_clicked)

    def sensor_clicked(self, index):
        print('clicked!  => ' + str(index))
        sensor = int(self.widgets.sensorList.item(index).text())
        sensor_values = self.session.query(Measurement).filter(Measurement.sensor_id == sensor). \
            order_by(Measurement.timestamp.desc()).limit(100).all()

        self.list_episodes = []
        current_starttime = sensor_values[0].timestamp
        current_episode = []
        for value in sensor_values:
            diff = (current_starttime - value.timestamp).seconds
            if diff < 60:
                current_episode.append(value)
            else:
                self.list_episodes.append(current_episode)
                current_episode = []
            current_starttime = value.timestamp
        if len(current_episode) > 0:
            self.list_episodes.append(current_episode)

        for episode in self.list_episodes:
            self.widgets.timeList.addItem(str(episode[0].timestamp).split('.')[0])

        print(f'Found {len(self.list_episodes)} different episodes')


    def episode_clicked(self, index):
        self.episode_index = index
        img_ar = np.array(self.list_episodes[self.episode_index][self.time_index].data).reshape((32,24))
        max_img = np.max(img_ar)
        min_img = np.min(img_ar)
        min_diff = max_img - min_img

        img_ar = ((img_ar - min_img)/min_diff) * 255
        rgb_img = np.zeros((32,24,3))
        rgb_img[:,:,0] = img_ar
        rgb_img[:, :, 1] = np.zeros((32,24))
        rgb_img[:, :, 2] = 255 - img_ar

        rgb_img = np.repeat(rgb_img, 20, axis=0)
        rgb_img = np.repeat(rgb_img, 20, axis=1)

        height, width, channel = rgb_img.shape
        bytesPerLine = 3 * width
        qImg = QImage(rgb_img.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
        pix = QPixmap.fromImage(qImg)
        self.widgets.imageLabel.setPixmap(pix)

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