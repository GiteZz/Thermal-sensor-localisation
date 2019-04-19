from localization.Person import Person
import numpy as np
from scipy.optimize import linear_sum_assignment
import time
class Tracker:
    def __init__(self):
        self.id_counter = 0
        self.persons = []
        self.visualisations = []
        self.last_tracker_timestamp = time.time()

    def add_visualisation(self,vis):
        assert(hasattr(vis, "tracker_update")) # must have update method to send new positions to
        self.visualisations.append(vis)

    def update(self, positions, timestamp):
        '''
        core function of the tracker
        links positions to existing or new persons
        updates all persons and creates new ones
        updates visualisation listeners
        :param timestamp: timestamp of positions
        :param positions: list of np arrays (x,y)
        :return: None
        '''
        timestamp = timestamp.timestamp()

        prob_matrix = self.get_matrix(positions,timestamp)
        tups, new_positions = self.get_assignment(prob_matrix)
        updated_pers_index = []
        for pers_index, pos_index in tups:
            filter = self.persons[pers_index].kalmanfilter
            filter.predict(timestamp)

            #if its not yet time to show, decrement TTS
            if self.persons[pers_index].TTS > 0:
                last_person_timestamp = self.persons[pers_index].kalmanfilter.previous_timestamp
                self.persons[pers_index].TTS -= (timestamp - last_person_timestamp)

            #rest the TTL to the initial value
            self.persons[pers_index].TTL = Person.TTL_initial_value

            filter.update(positions[pos_index],timestamp)
            updated_pers_index.append(pers_index)
        
        #decrement all the other Person's TTL
        for pers_index in range(len(self.persons)):
            if pers_index not in updated_pers_index:
                self.persons[pers_index].TTL -= (timestamp - self.last_tracker_timestamp)
                if self.persons[pers_index].TTL <=0:
                    del self.persons[pers_index]
                
        for pos_index in new_positions:
            self.persons.append(Person(self.id_counter,positions[pos_index],timestamp))
            self.id_counter+=1

        self.visualisations_update()
        #print("tracker updated")

    def get_matrix(self,positions,timestamp):
        '''
        creates probability matrix for all persons and positions
        :param positions: see update
        :return: to be specified
        '''

        matrix = np.zeros((len(self.persons),len(positions)))
        for i in range(len(self.persons)):
            for j in range(len(positions)):
                matrix[i,j]= self._prob(self.persons[i].kalmanfilter.x[0:2],positions[j])
        return matrix


    def get_assignment(self,prob_matrix):
        '''
        makes global optimal assignment of the prop matrix
        :param prob_matrix:
        :return: a tuple , first part is an array of tupples person_index, position_index
                second part are just positions
        '''
        person_index, position_index = linear_sum_assignment(prob_matrix)
        tups = zip(person_index,position_index)
        new_objects = []
        for i in range(prob_matrix.shape[1]):
            if not i in position_index:
                new_objects.append(i)
        return tups,new_objects

    def visualisations_update(self):
        '''
        sends new positions to listeners
        :return:
        '''
        vis_dict = {}
        for person in self.persons:
            if person.TTS <= 0:
                sp1 = round(person.kalmanfilter.x[2], 2)
                sp2 = round(person.kalmanfilter.x[3], 2)
                ttl_round = round(person.TTL, 2)
                vis_dict[person.ID] = {'position':person.get_location(), 'timelived': ttl_round, 'v_x': sp1, 'v_y': sp2}
            

        for vis_object in self.visualisations:
            vis_object.tracker_update(vis_dict)


    def _prob(self, x, y):
        '''
        for the moment this is just the euclidean distance
        :param x: 2D np array
        :param y: 2D np array
        :return:
        '''
        return np.sum(np.power(x-y,2))
        #TODO: tresh the distance
        #perhaps on two*sigma

    def __repr__(self):
        s = ("____TRACKER STATE_____ \n")
        for person in self.persons:
            s += person.__repr__()
            s += "\n"
        return s

    def reset_tracker(self):
        '''
        This function resets the whole state of the tracker
        '''
        self.id_counter = 0
        self.persons = []
        self.visualisations = []
        self.last_tracker_timestamp = time.time()


if __name__ == "__main__":
    t0 = time.time()

    t = Tracker()
    t.update([np.array([1.,2])], t0)
    print(t)
    t.update([np.array([2.,3]), np.array([5.,6])], t0 + 1)
    print(t)
    t.update([np.array([3.,4]), np.array([3.,5])], t0 + 2)
    print(t)
    t.update([ np.array([5.,6])], t0 + 3)
    print(t)