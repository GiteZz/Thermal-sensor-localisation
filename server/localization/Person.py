from localization.Adapted_Kalman import AdaptedKalmanFilter
import numpy as np

class Person:

    TTL_initial_value = 10
    TTS_initial_value = 1

    def __init__(self,ID,pos,timestamp):
        self.time_to_show = 5 # time before being considered as a "valid" person  in seconds
        self.ID = ID
        self.kalmanfilter = AdaptedKalmanFilter(pos,timestamp)
        self.locations = {timestamp:pos} #dicts automatic ordered!
        self.locations.setdefault(None)

        self.TTL = Person.TTL_initial_value
        self.TTS = Person.TTS_initial_value

    def __repr__(self):
        return (f"{self.ID} => loc = {self.kalmanfilter.x[0]},{self.kalmanfilter.x[1]}"
              f" speed = {self.kalmanfilter.x[2]},{self.kalmanfilter.x[3]} at {self.kalmanfilter.previous_timestamp}")

    def get_location(self):
        return self.kalmanfilter.get_location()



if __name__ == "__main__":
    p = Person(1,np.array([0.,0]),0)
    print(p)
    print("--")