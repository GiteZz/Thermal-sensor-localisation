import numpy as np
from help_module.csv_reader import read_data

def generate_mask(data):
    data=np.array(data)[:,0]
    print(data[115])
    return



data=read_data('sensor_data_21-02.csv',400,871)
mask=generate_mask(data)
print(mask)
