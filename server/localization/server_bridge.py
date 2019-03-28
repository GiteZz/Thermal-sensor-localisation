from localization.tracker import Tracker
from localization.localiser import Localiser
from help_module.calibration_helper import save_calibration_data

class ServerBridge:
    def __init__(self):
        self.localization_dict = {}
        self.tracker = Tracker()
        self.calibrate_data = []
        self.current_calibrate = None
        self.auto_localiser = True

    def update(self, sensor_id, data, timestamp):
        self.check_updates(sensor_id, data, timestamp)
        if sensor_id not in self.localization_dict:
            self.add_localiser(sensor_id)
        self.localization_dict[sensor_id].update(data, timestamp)

    def add_localiser(self, sensor_id, calibrate_data=None):
        new_localiser = Localiser()
        if calibrate_data is not None:
            new_localiser.calibrate(calibrate_data)
        new_localiser.set_tracker(self.tracker)

        self.localization_dict[sensor_id] = Localiser()

    def calibrate_point(self,name,  co):
        if self.current_calibrate is None:
            self.current_calibrate = {'name': name, 'co': co, 'img_data': {}}
        else:
            print('WARNING there is still a calibration point active')

    def check_updates(self, sensor_id, data, timestamp):
        self.check_calibrate(sensor_id, data, timestamp)

    def check_calibrate(self, sensor_id, data, timestamp):
        if self.current_calibrate is not None:
            amount_active_sensors = len(self.localization_dict)
            if sensor_id not in self.current_calibrate['img_data']:
                self.current_calibrate['img_data'][sensor_id] = data

            if len(self.current_calibrate['img_data']) == amount_active_sensors:
                self.calibrate_data.append(self.current_calibrate)
                self.current_calibrate = None

    def bridge_save_cal_data(self):
        save_calibration_data(self.calibrate_data)
        print("Saved loc data")

