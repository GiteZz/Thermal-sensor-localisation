from filterpy.kalman import KalmanFilter
import numpy as np
import datetime

class AdaptedKalmanFilter(KalmanFilter):
    '''
    This class Extends the Kalman to allow for irregular time intervals
    '''
    def __init__(self,position, timestamp,dim_x = 4,dim_z = 2):
        '''
        constructor
        :param dim_x: number of state variables
        :param dim_z: number of measurment variables
        :param position: current 2D position and velocity
        :param timestamp: current timestamp
        '''
        super().__init__(dim_x,dim_z)
        self.x[0] = position[0]
        self.x[1] = position[1]
        #TODO: set initial speed.. (perhaps leave at zero?)
        self.previous_timestamp = timestamp
        self.time_difference = 0

        self.time_lived = 0

        #TODO: add ,H,P,Q,R
        #TODO: F should use time_difference to update x using dx/dt
        self.B = np.zeros(1) #no controller actions
        self.u = np.zeros((1)) #no controller actions
        self.F = np.eye(dim_x) # velocity is updated in update_time_diff
        #temp to test update!
        self.H[0,0] = 1
        self.H[1,1] = 1
        ####


    def predict(self,timestamp):
        self.__update_timedifference(timestamp)
        super().predict()

    def get_prediction(self,timestamp):
        '''
        this function performs a prediction without actually changing the internal state
        this allows to do multiple predictions (for different timestamps) before deciding
        which timestamp is definitive one and update the state
        :param timestamp: timestamp of the prediction you want
        :return: (x,P) with x the internal state and P the covariance matrix
        '''
        self.__update_timedifference(timestamp)
        return super().get_prediction()

    def update(self,z, timestamp):
        '''
        updates just like normal Kalman but sets time difference first and sets previous
        timestamp after update
        :param z: measurement
        :param timestamp: timestamp of the measurement
        :return:
        '''
        self.__update_timedifference(timestamp)
        super().update(z)
        self.time_lived+= self.time_difference #add time to time lived
        self.previous_timestamp = timestamp #update internal timestamp
        self.time_difference = 0

    def batch_filter(self, zs, ts):
        '''
        allows to give the filter an array of measurements and get results
        :param zs: array of measurements
        :param ts: array of timestamps (same dim)
        :return:  (means, P, means_predict, P_predict)
        '''
        assert(len(ts) == len(zs))

        fs = []
        for time in ts: #create array of F matrices
            self.__update_timedifference(time)
            fs.append(self.F)
        return super().batch_filter(zs,fs)

    def __update_timedifference(self,timestamp):
        self.time_difference = timestamp - self.previous_timestamp
        # TODO: convert to seconds, for now all is considered to be seconds.
        self.F[0, 2] = self.time_difference
        self.F[1, 3] = self.time_difference

    def get_location(self):
        return self.x[0][0], self.x[1][0]

if __name__ == "__main__":
    KF = AdaptedKalmanFilter(np.array([0.,0]),0)
    print(KF.get_prediction(12))
    KF.predict(12)
    print(KF.x)
    KF.update(np.array([10.,17]),12)
    print(KF.x)
    KF.predict(24)
    print(KF.x)
    KF.update(np.array([10., 17]), 24) #simulate stopping
    print(KF.x)
