from help_module.img_processing_helper import ImageProcessor
import numpy as np
import math
class Localiser (ImageProcessor):
    def __init__(self):
        ImageProcessor.__init__(self)
        self.data_height=175
        self.sensor_height=0
        self.sensor_center=(0,0)
        self.origin_corner=(0,0) #corner for which centroid would be (0,0)
        #from documentation, in top view this is the right upper corner with respect to the notch

        self.absolute_positions=[]
        self.rotmatrix=np.matrix(np.zeros((2,2)))
        self.transmatrix=np.matrix(np.zeros((2,1)))

    def __determine_transformation_matrix(self):
        #angle between system of the room and relative system
        angle= math.atan((self.center[1]-self.origin_corner[1])/(self.center[0]-self.origin_corner[0]))-math.atan(12/16)
        c,s=math.cos(angle),math.sin(angle)
        self.rotmatrix=np.matrix([[c,-s],[s,c]])
        self.transmatrix=np.matrix([[c,-s],[s,c]])*np.matrix([[-16],[-12]])+np.matrix([[self.center[0]],[self.center[1]]])

    def set_corner_and_center(self,corner,center):
        '''
        set the absolute positioning of the sensor
        :param corner: in centimeter! choose correct corner (closest to the room coordinate system origin (right upper from notch
        :param center: in centimeter!
        :return:
        '''
        self.center=center
        if corner[0]<center[0] and corner[1]<center[1]: #origin corner under assumption of small angle!
            self.origin_corner=corner
        else:
            raise NotImplementedError
        self.__determine_transformation_matrix()

    def get_error(self,height):
        '''
        check accuracy of measurements
        :param height: height in CM of sensor to the floor
        :return: sqaure of the difference between the two calculation methods
        '''
        dst=math.sqrt((self.center[0]-self.origin_corner[0])**2+(self.center[1]-self.origin_corner[1])**2)
        x=math.sin(55)*(height-self.data_height) #subtract human body length from ceiling height
        y=math.sin(35)*(height-self.data_height)
        calc_dst=math.sqrt(x**2+y**2)
        err=dst-calc_dst
        return err

    def get_abs_locations(self):
        '''
        essential function of this class: calculates absolute position of the blobs in the current frame
        :return: returns an array of absolute locations
        '''
        centroids=np.array(self.centroids)
        self.absolute_positions=[]
        for centroid in centroids:
            centroid=self.rotmatrix*centroid.reshape((2,1))+self.transmatrix
            centroid=np.array(centroid).astype(np.uint16).reshape((1,2))
            self.absolute_positions.append([centroid[0][0],centroid[0][1]])
        return self.absolute_positions










