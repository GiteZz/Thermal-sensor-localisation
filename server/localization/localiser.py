import cv2
import numpy as np
import json
from localization.processing import ImageProcessor

class Localiser:
    def __init__(self, sensor_id):
        self.sensor_id=sensor_id
        self.matrix=[]
        self.calibration_points=[] # key=px_index, val=world_coord
        self.tracker = None
        self.processor = ImageProcessor()
        self.com_module = None
        # if this flag is true, all centroids are converted to world coords before
        # sending to the tracker
        self.WORLD_CORDS_FLAG = True
        self.calibrated = False

    def __add_calibration_point(self,cam_x,cam_y,world_x,world_y):
        self.calibration_points.append([[cam_x,cam_y],[world_x,world_y]])

    def __add_calibration_array(self,left_x,left_y,right_x,right_y,n):
        for i in range(n):
            x_i=left_x+i/n*right_x
            y_i=left_y +i/n*right_y
            self.__add_calibration_point(self,x_i,y_i)

    def __determine_matrix(self):
        assert(len(self.calibration_points)>=4)
        self.calibration_points=np.array(self.calibration_points).astype(np.float32)
        self.matrix,h=cv2.findHomography(self.calibration_points[:,0],self.calibration_points[:,1])
        return self.matrix

    def __update_world_co(self, centroids):
        # each value in centroids should be a pair (loc, timestamp)
        self.tracker.update(centroids)

    def get_world_cords(self, points):
        if len(self.matrix) ==0:
            print("not yet callibrated")
        else:
            world_cords = []
            for point in points:
                vec = np.array([point[0],point[1],1])
                cord = np.matmul(self.matrix,np.transpose(vec))
                cord *= 1/cord[2]
                world_cords.append(cord[0:2])
            return world_cords

    def calibrate_data(self):
        print("Calibrating data")
        with open('configuration_files/calibration_configuration.json', 'r') as f:
            print("opened file")
            config = json.load(f)
            data=config['calibration_data']
            print(data)
            for key,value in data.items():
                debug = value.get(str(self.sensor_id),None)
                if value.get(str(self.sensor_id),None):
                    debug = min(value.get(str(self.sensor_id)))
                    if min(value.get(str(self.sensor_id)))>0:
                        #if <0 this point is not seen by the sensor
                        img_cord=value.get(str(self.sensor_id))
                        world_cord=config["points"][key]
                        self.__add_calibration_point(img_cord[0],img_cord[1],world_cord[0],world_cord[1])
                        print('calibration points added for '+str(self.sensor_id))
        self.__determine_matrix()
        self.calibrated = True
        print(self.calibration_points)

    def set_tracker(self, tracker):
        self.tracker = tracker

    def set_com_module(self, com_module):
        self.com_module = com_module

    def update(self, data, timestamp):
        self.processor.set_thermal_data(data)
        if self.com_module is not None and self.com_module.any_clients():
            imgs = self.processor.get_imgs()
            self.com_module.distribute_imgs(self.sensor_id, imgs)
        if not self.WORLD_CORDS_FLAG:
            print('img cords update by localiser')
            self.tracker.update(self.processor.get_centroids(), timestamp)
        else:
            if self.calibrated:
                print('world cord update by localiser')
                self.tracker.update(self.get_world_cords(self.processor.get_centroids()),timestamp)




if __name__=='__main__':
    loc=Localiser(65)
    loc.calibrate_data()
    print(loc.get_world_cords([[194,79],[194,90]]))
    print(loc.calibrated)


