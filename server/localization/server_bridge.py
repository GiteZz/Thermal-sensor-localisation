from localization.tracker import Tracker
from localization.localiser import Localiser

class ServerBridge:
    def __init__(self):
        self.localization_dict = {}
        self.tracker = Tracker()
        self.calibrate_data = []
        self.current_calibrate = None

    def update(self, sensor_id, data, timestamp):
        self.check_updates(sensor_id, data, timestamp)
        if sensor_id in self.localization_dict:
            self.localization_dict[sensor_id].update(data, timestamp)
        else:
            raise Exception('Sensor doesn\'t have a Localiser')

    def add_localiser(self, sensor_id, calibrate_data=None):
        new_localiser = Localiser()
        if calibrate_data is not None:
            new_localiser.calibrate(calibrate_data)
        new_localiser.set_tracker(self.tracker)

        self.localization_dict[sensor_id] = Localiser()

    def calibrate_point(self, co):
        if self.current_calibrate is None:
            self.current_calibrate = {'co': co, 'img_data': {}}
        else:
            print('WARNING there is still a calibration point active')


    def check_updates(self, sensor_id, data, timestamp):
        self.check_calibrate(sensor_id, data, timestamp)

    def check_calibrate(self, sensor_id, data, timestamp):
        if self.current_calibrate is not None:
            amount_active_sensors = len(self.localization_dict)
            if sensor_id not in self.current_calibrate['img_data']:
                processor=self.localization_dict[sensor_id].processor
                assert(len(processor.centroids) == 1)
                self.current_calibrate['img_data'][sensor_id] = processor.centroids[0]

            if len(self.current_calibrate['img_data']) == amount_active_sensors:
                self.calibrate_data.append(self.current_calibrate)
                self.current_calibrate = None

