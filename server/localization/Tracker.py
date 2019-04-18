from localization.Person import Person
import numpy as np

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
        prob_matrix = self.get_matrix(positions)
        tups, new_positions = self.get_assignment(prob_matrix)
        for pers_index,pos_index in tups:
            filter = self.persons[pers_index].kalmanfilter
            filter.predict(timestamp)
            filter.update(positions[pos_index],timestamp)
        for pos_index in new_positions:
            self.persons.append(Person(self.id_counter,positions[pos_index],timestamp))
        self.visualisations_update()

    def get_matrix(self,positions):
        '''
        creates probability matrix for all persons and positions
        :param positions: see update
        :return: to be specified
        '''
        raise NotImplementedError

    def get_assignment(self,prob_matrix):
        '''
        makes global optimal assignment of the prop matrix
        :param prob_matrix:
        :return: a tuple , first part is an array of tupples person_index, position_index
                second part are just positions
        '''
        raise NotImplementedError

    def visualisations_update(self):
        '''
        sends new positions to listeners
        :return:
        '''
        for person in self.persons:
            person.get_location()

    def __repr__(self):
        s = ("____TRACKER STATE_____ \n")
        for person in self.persons:
            s += person.__repr__()
        return s


if __name__ == "__main__":
    t = Tracker()
    t.persons.append(Person(1,np.array([1.0,0]),0))
    print(t)