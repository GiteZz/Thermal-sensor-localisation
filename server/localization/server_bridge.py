from localization.tracker import Tracker
from localization.localizer import Localiser

class ServerBridge:
    def __init__(self):
        self.localization_dict = {}
        self.tracker = Tracker()

    def update(self, sensor_id, data, timestamp):
        if sensor_id in self.localization_dict:
            self.localization_dict[sensor_id].update(data, timestamp)
        else:
            raise Exception('Sensor doesn\'t have a Localiser')

    def add_localiser(self, sensor_id, calibrate_data=None):
        self.localization_dict[sensor_id] = Localiser(calibrate_data)
