import numpy as np
from help_module.csv_helper import read_data
from help_module.img_helper import convert_to_thermal_image
from help_module.flask_helper import serve_pil_image


def clean_data(data):
    cleaned=[]
    for frame in data:
        if min(frame)>10 and max(frame) <45:
            cleaned.append(frame)
    print('total frames='+str(len(data))+',useful frames:'+str(len(cleaned)))
    return np.array(cleaned)

def generate_mask(data,max_corr=6):
    data=np.array(data)[:,0]
    data=clean_data(data)
    data.flatten()
    mean=np.mean(data,0)
    mask= mean- min(mean)
    max=np.max(mask)
    if max> max_corr:
        mask*=(max_corr/max)
    return mask



data=read_data('sensor_data_21-02.csv',400,871)
mask=generate_mask(data)
print(mask)
im1=convert_to_thermal_image(data[45][0],1,True)
im2=convert_to_thermal_image(data[45][0]-mask,1,True)
#TODO
#display both to compare them and find a frame with persons in it to apply the mask