#query used to obtain the csv
'''
select data, timestamp ,"sequence_ID", "sensor_ID"
from public."Sensor_data"
where "sensor_ID"=51
order by timestamp, "sequence_ID"
'''


import csv
import numpy as np
import matplotlib.pyplot as plt

def process_csv_row(row):
    return [np.array(eval(row[0])),row[1], eval(row[2]),eval(row[3])]

def read_data(a,b):
    with open('sensor_data_21-02.csv','r') as csvfile:
        reader=csv.reader(csvfile,delimiter=',')
        data=[]
        for index,row in enumerate(reader):
            if a<index and index <b:
                data.append(process_csv_row(row))
        return data

data=read_data(2490,2790)

d=np.histogram(data[2][0])
print(d)
for i in range(298):
    plt.hist(data[i][0])
plt.show()










import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from collections import OrderedDict
from matplotlib import cm


