import csv
import numpy as np

def process_csv_row(row):
    return [np.array(eval(row[0])),row[1], eval(row[2]),eval(row[3])]

def read_data(filename,start=0,end=None):
    with open(filename,'r') as csvfile:
        reader=csv.reader(csvfile,delimiter=',')
        data=[]
        if end is None:
            end=10000000 #random high value
        for index,row in enumerate(reader):
            if start<index and index <end:
                data.append(process_csv_row(row))
        return data