from localization.tracker import Tracker
from localization.localiser import Localiser
from localization.com_module import ComModule
from help_module.calibration_helper import save_calibration_data

class ServerBridge:
    def __init__(self):
        self.localization_dict = {}
        self.tracker = Tracker()
        self.com_module = ComModule()
        self.calibrate_data = []
        self.current_calibrate = None
        self.auto_localiser = True

    def update(self, sensor_id, data, timestamp):
        """
        This is the main input of the ServerBridge, accepts thermal input and will send is the a localiser.
        :param sensor_id:
        :param data:
        :param timestamp:
        :return:
        """
        self.check_updates(sensor_id, data, timestamp)
        if sensor_id not in self.localization_dict:
            self.__add_localiser(sensor_id)
        self.localization_dict[sensor_id].update(data, timestamp)

    def __add_localiser(self, sensor_id, calibrate_data=None):
        """
        Creates new Localiser and add the tracker
        TODO: how to do calibration?
        :param sensor_id:
        :param calibrate_data:
        :return:
        """
        new_localiser = Localiser(sensor_id)
        # if calibrate_data is not None:
        #     new_localiser.calibrate(calibrate_data)
        new_localiser.set_tracker(self.tracker)
        new_localiser.set_com_module(self.com_module)

        self.localization_dict[sensor_id] = new_localiser

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
                processor=self.localization_dict[sensor_id].processor
                processor.process(data)
                print(f'amount of centroid: {len(processor.centroids)}')
                if len(processor.centroids) == 1:
                    self.current_calibrate['img_data'][sensor_id] = processor.centroids[0]
                else:
                #this means the sensor does not "see" this frame so we put an arbitrary negative value
                    self.current_calibrate['img_data'][sensor_id]=[-1,-1]


            if len(self.current_calibrate['img_data']) == amount_active_sensors:
                print("Saved the calibration point")

                self.calibrate_data.append(self.current_calibrate)
                save_calibration_data(self.calibrate_data)
                self.current_calibrate = None

    def bridge_save_cal_data(self):
        save_calibration_data(self.calibrate_data)
        print("Saved loc data")

