from localization.Person import Person
import numpy as np
from scipy.optimize import linear_sum_assignment

class Tracker:
    def __init__(self):
        self.id_counter = 0
        self.persons = []
        self.visualisations = []

    def add_visualisation(self,vis):
        assert(hasattr(vis,"tracker_update")) # must have update method to send new positions to
        self.visualisations.append(vis)

    def update(self,timestamp, positions):
        '''
        core function of the tracker
        links positions to existing or new persons
        updates all persons and creates new ones
        updates visualisation listeners
        :param timestamp: timestamp of positions
        :param positions: list of np arrays (x,y)
        :return: None
        '''
        prob_matrix = self.get_matrix(positions,timestamp)
        tups, new_positions = self.get_assignment(prob_matrix)
        for pers_index,pos_index in tups:
            filter = self.persons[pers_index].kalmanfilter
            filter.predict(timestamp)
            filter.update(positions[pos_index],timestamp)
        for pos_index in new_positions:
            self.persons.append(Person(self.id_counter,positions[pos_index],timestamp))
            self.id_counter+=1
        self.visualisations_update()

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
        for person in self.persons:
            person.get_location()
        #TODO

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


if __name__ == "__main__":
    t = Tracker()
    t.update(0,[np.array([1.,2])])
    print(t)
    t.update(1,[np.array([2.,3]), np.array([5.,6])])
    print(t)
    t.update(2,[np.array([3.,4]), np.array([3.,5])])
    print(t)
    t.update(3,[ np.array([5.,6])])
    print(t)