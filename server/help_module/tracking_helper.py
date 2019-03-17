from help_module.img_processing_helper import ImageProcessor
import numpy as np
import math
class Localiser (ImageProcessor):
    def __init__(self):
        ImageProcessor.__init__(self)
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
        self.center=center
        if corner[0]<center[0] and corner[1]<center[1]: #origin corner under assumption of small angle!
            self.origin_corner=corner
        else:
            raise NotImplementedError
        self.__determine_transformation_matrix()

    def get_abs_locations(self):
        centroids=np.array(self.centroids)
        self.absolute_positions=[]
        for centroid in centroids:
            centroid=self.rotmatrix*centroid.reshape((2,1))+self.transmatrix
            centroid=np.array(centroid).astype(np.uint16).reshape((1,2))
            self.absolute_positions.append([centroid[0][0],centroid[0][1]])
        return self.absolute_positions










