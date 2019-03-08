from help_module.csv_helper import read_data
from help_module.img_processing_helper import Img_processor
import matplotlib.pyplot as plt
'''
this test file contains an absolute path, please change this path to test the module on your pc
'''

num=300
data=read_data(r'C:\Users\Thomas\Documents\School\VOP\VOP\server\data_vis\files\sensor_data_episode_20190221-143435_0.csv',0,502)
#manually selected empty frames of this episode
img_processor=Img_processor()
print(data[num][0])
plt.subplot(2,1,1).pcolor(data[num][0].reshape((24,32)))
res=img_processor.process(data[num][0])
plt.subplot(2,1,2).imshow(res)

plt.show()