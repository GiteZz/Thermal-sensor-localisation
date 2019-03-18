from help_module.localisation_helper import Localiser
import numpy as np

class Tracker:
    def __init__(self,window=10):
        self.ID_COUNTER=1 #generates unique ID's
        self.WINDOW=window
        self.current_positions={} # ID: (x,y)
        self.prev_positions= [] # [ {ID: (x,y)} ] index in array= number of frames between current and this frame

        self.out_of_frame={}
        self.current_centroids=[]

        self.localisers={} #sensor_ID: Localiser()
    def __update_current_centroids(self):
        raise NotImplementedError

    def __remove_dupl_centroids(self):
        raise NotImplementedError

    def __get_likelihood(self):
        raise NotImplementedError

    def __map_current_centroids(self,MLmatrix):
        raise NotImplementedError
    def __update_out_of_frame(self):
        raise NotImplementedError

    def add_sensor(self,ID):
        if not self.localisers.get(ID,False):
            self.localisers.update({ID:Localiser()})
        else:
            raise KeyError

    def reset_tracker(self):
        self.ID_COUNTER=1
        self.current_positions = {}
        self.prev_positions = []
        self.out_of_frame = {}
        self.current_centroids = []

    def update(self):
        self.__update_current_centroids()
        self.__remove_dupl_centroids()
        MLmatrix=self.__get_likelihood()
        self.__map_current_centroids(MLmatrix)
        self.__update_out_of_frame()
        return self.current_positions

