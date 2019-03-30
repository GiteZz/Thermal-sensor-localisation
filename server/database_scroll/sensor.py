from PyQt5.QtWidgets import QGraphicsScene, QFileDialog, QCheckBox, QLabel, QHBoxLayout
from help_module.csv_helper import load_csv
from help_module.data_model_helper import Measurement, Base, CSV_Measurement


class Sensor:
    def __init__(self, db_bridge, app):
        self.db_bridge = db_bridge
        self.app = app

        self.layout = None
        self.label = None
        self.checkbox = None

        self.checkbox_callback = None

    def set_sensor_values(self, sensor_type, sensor_id=None, file_name=None, data=None):
        self.sensor_type = sensor_type
        self.data = data
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
        return self.data is not None

    def reload(self):
        if self.data is not None:
            self.load_data()

    def is_active(self):
        return self.checkbox.isChecked()

    def get_data(self):
        if self.data is None:
            print("WARNING attempting to load data that is not loaded")
        return self.data

    def load_data(self):
        """
        This function takes a source and then looks at its type to find the function to get that data

        :param source: A dict containing all the information to load the data
        :return: list of measurements
        """
        if self.sensor_type == 'csv':
            self.data = load_csv(self.file_name)
        elif self.sensor_type == 'sensor':
            self.data = self.load_sensor()
        else:
            raise Exception('Source type was not recognized')

    def load_sensor(self):
        """
        Uses a database query to get measurements from the sensor with id == sensor_id

        :param sensor_id:
        :return:
        """
        param = self.app.get_query_param()
        return self.db_bridge.get_values(self.sensor_id, param)


