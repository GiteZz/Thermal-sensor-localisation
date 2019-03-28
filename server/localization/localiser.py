import cv2
import numpy as np
from help_module.img_processing_helper import ImageProcessor
class Localiser:
    def __init__(self):
        self.matrix=[]
        self.calibration_points=[] # key=px_index, val=world_coord
        self.tracker = None
        self.processor = ImageProcessor()

    def add_calibration_point(self,cam_x,cam_y,world_x,world_y):
        self.calibration_points.append([[cam_x,cam_y],[world_x,world_y]])

    def add_calibration_array(self,left_x,left_y,right_x,right_y,n):
        for i in range(n):
            x_i=left_x+i/n*right_x
            y_i=left_y +i/n*right_y
            self.add_calibration_point(self,x_i,y_i)

    def determine_matrix(self):
        assert(len(self.calibration_points)>=4)
        self.calibration_points=np.array(self.calibration_points).astype(np.float32)
        self.matrix,h=cv2.findHomography(self.calibration_points[:,0],self.calibration_points[:,1])
        return self.matrix

    def get_world_coords(self, cam_x,cam_y):
        return np.matmul(self.matrix,np.transpose(np.array([cam_x,cam_y,1])))

#TODO: communicate with Gilles to determine purpose of these functions
    def calibrate_data(self):
        raise NotImplementedError

    def set_tracker(self, tracker):
        self.tracker = tracker

    def update(self, data, timestamp):
        pass
        # raise NotImplementedError

    def update_world_co(self, centroids):
        # each value in centroids should be a pair (loc, timestamp)
        self.tracker.update(centroids)

if __name__=='__main__':
    H=Localiser()
    #points 5,7,8,9,10,11
    H.add_calibration_point(143,74,210,304)
    H.add_calibration_point(265,29,106,32)
    H.add_calibration_point(264,115,287,83)
    H.add_calibration_point(126,164,345,337)
    H.add_calibration_point(112,31,128,342)
    H.add_calibration_point(44,124,272,481)
    m=H.determine_matrix()
    cord=H.get_world_coords(44,124)
    cord/=cord[2]
    print(str(cord) +'vs' +'(272,481)')

    cord = H.get_world_coords(264, 115)
    cord /= cord[2]
    print(str(cord) + 'vs' + '(287,83)')

    cord = H.get_world_coords(265, 29)
    cord /= cord[2]
    print(str(cord) + 'vs' + '(106,32)')

    cord = H.get_world_coords(143, 74)
    cord /= cord[2]
    print(str(cord) + 'vs' + '(210,304)')
    cord = H.get_world_coords(126, 164)
    cord /= cord[2]
    print(str(cord) + 'vs' + '(345,337)')
    # new points
    cord = H.get_world_coords(72, 75)
    cord /= cord[2]
    print(str(cord) + 'vs' + '(199,415)')


