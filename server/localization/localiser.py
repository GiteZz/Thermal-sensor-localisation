import cv2
import numpy as np
import json
from help_module.img_processing_helper import ImageProcessor
class Localiser:
    def __init__(self,sensor_id):
        self.sensor_id=sensor_id
        self.matrix=[]
        self.calibration_points=[] # key=px_index, val=world_coord
        self.tracker = None
        self.processor = ImageProcessor()

    def __add_calibration_point(self,cam_x,cam_y,world_x,world_y):
        self.calibration_points.append([[cam_x,cam_y],[world_x,world_y]])

    def __add_calibration_array(self,left_x,left_y,right_x,right_y,n):
        for i in range(n):
            x_i=left_x+i/n*right_x
            y_i=left_y +i/n*right_y
            self.add_calibration_point(self,x_i,y_i)

    def __determine_matrix(self):
        assert(len(self.calibration_points)>=4)
        self.calibration_points=np.array(self.calibration_points).astype(np.float32)
        self.matrix,h=cv2.findHomography(self.calibration_points[:,0],self.calibration_points[:,1])
        return self.matrix

    def __update_world_co(self, centroids):
        # each value in centroids should be a pair (loc, timestamp)
        self.tracker.update(centroids)

    def get_world_cords(self, cam_x,cam_y):
        if len(self.matrix) ==0:
            print("not yet callibrated")
        else:
            return np.matmul(self.matrix,np.transpose(np.array([cam_x,cam_y,1])))

    def calibrate_data(self):
        with open('configuration_files/calibration_configuration.json', 'r') as f:
            config = json.load(f)
            data=config['calibration_data']
            for key,value in data.items():
                if value.get(self.sensor_id,None) and min(value.get(self.sensor_id))>0: #if <0 this point is not seen by the sensor
                    img_cord=value.get(self.sensor_id)
                    world_cord=config["points"][key]
                    self.__add_calibration_point(img_cord[0],img_cord[1],world_cord[0],world_cord[1])
        print('calibration points added for '+str(self.sensor_id))
        self.__determine_matrix()


    def set_tracker(self, tracker):
        self.tracker = tracker

    def update(self, data, timestamp):
        self.processor.process(data)
        self.tracker.update(self.processor.centroids, timestamp)



if __name__=='__main__':
    loc=Localiser(243)
    loc.calibrate_data()


