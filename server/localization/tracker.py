from help_module.localisation_helper import point_dist, point_line_diff
import numpy as np
from numpy.linalg import norm as vec_norm
from localization.person import Person
import math

class Tracker:

    SAME_OBJECT_TRESHHOLD = 0.6
    NEW_OBJECT_TRESSHOLD = 0.6

    def __init__(self):
        self.ID_COUNTER = 0 #generates unique ID's

        self.current_persons = []
        self.edges = []

    def update(self, centroids, timestamp):
        for centroid in centroids:
            if centroid is not np.ndarray:
                raise Exception('Expected numpy array as data type')
            self.centroid_update(centroid, timestamp)

    def centroid_update(self, centroid, timestamp):
        closest_persons = self.get_closest_centroids(centroid, 2)

        highest_prob = 0
        best_person = None
        for person in closest_persons:
            prob = self.get_equal_prob(centroid, person, timestamp)
            if prob > highest_prob:
                highest_prob = prob
                best_person = person

        if highest_prob > self.SAME_OBJECT_TRESHHOLD:
            best_person.add_location(centroid, timestamp)
        else:
            new_prob = self.get_new_prob(centroid)
            new_pers = Person()
            new_pers.add_location(centroid, timestamp)
            self.current_persons.append(new_pers)
            if new_prob > self.NEW_OBJECT_TRESSHOLD:
                print("HIGH probability of new person")
            else:
                print("LOW probability of new person")


    def get_new_prob(self, centroid):
        offset = 1
        dst_list = [point_line_diff(line, centroid) for line in self.edges]
        min_dst = min(dst_list)

        return (math.atan(-min_dst + offset) + math.pi / 2) / math.pi


    def get_closest_centroids(self, centroid, amount):
        distances = {}
        for person in self.current_persons:
            distances[person] = point_dist(person.loc, centroid)

        sorted_list = sorted(distances, key=distances.__getitem__)

        return sorted_list[0:amount]

    def get_equal_prob(self, current_loc, person, timestamp):
        prev_loc_1 = person.get_closest_loc(timestamp, 1)
        prev_loc_2 = person.get_closest_loc(timestamp, 2)

        prev_mov_vec = prev_loc_2 - prev_loc_1
        cur_mov_vec = prev_loc_1 - current_loc

        prev_dist = vec_norm(prev_mov_vec)
        cur_dist = vec_norm(cur_mov_vec)

        angle_diff = math.acos((prev_mov_vec @ cur_mov_vec) / (prev_dist * cur_dist))

        p_dst = self.distance_prob(cur_dist, prev_dist)
        p_angle = self.angle_prob(angle_diff)

        fac = self.angle_dist_fac(cur_dist)

        return (1 - fac) * p_dst + fac * p_angle

    def distance_prob(self, new_dist, cur_dist):
        sigma = 5

        top = (new_dist - cur_dist) ** 2
        bottom = 2 * (sigma ** 2)

        return math.exp(-(top/bottom))

    def angle_dist_fac(self, value):
        offset = 1
        return (math.atan(value - offset) + math.pi/2) / math.pi

    def angle_prob(self, angle_diff):
        sigma = 5
        return math.exp(-(angle_diff ** 2) / (2 * (sigma ** 2)))

    def add_edge(self, edge):
        self.edges.append(edge)