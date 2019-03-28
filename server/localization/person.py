from help_module.time_helper import abs_diff
from datetime import timedelta


class Person:
    def __init__(self, centroid, timestamp):
        self.remove_time = 2
        self.locations = []
        self.appear_loc = centroid
        self.add_location(centroid, timestamp)

    def add_location(self, loc, timestamp):
        self.locations.append((loc, timestamp))

    def get_prev_location(self):
        if len(self.locations) == 0:
            return None
        else:
            return self.locations[-1][0]

    def get_closest_loc(self, timestamp, second_diff):
        compare_time = timestamp - timedelta(seconds=second_diff)
        min = float('inf')
        min_loc = None
        for loc in self.locations:
            diff = abs_diff(compare_time, loc[1])
            if diff < min:
                min = diff
                min_loc = loc[0]

        return min_loc