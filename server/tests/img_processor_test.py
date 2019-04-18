# from help_module.csv_helper import read_data
# from help_module.img_processing_helper import ImageProcessor
# import matplotlib.pyplot as plt
'''
this test file contains an absolute path, please change this path to test the module on your pc
'''

# num=300
# data=read_data(r'C:\Users\Thomas\Documents\School\VOP\VOP\server\data_vis\files\sensor_data_episode_20190221-143435_0.csv',0,502)
# #manually selected empty frames of this episode
# img_processor=ImageProcessor()
# print(data[num][0])
# plt.subplot(2,1,1).pcolor(data[num][0].reshape((24,32)))
# img_processor.process(data[num][0])
# res=img_processor.plot_frame()
# plt.subplot(2,1,2).imshow(res)
#
# plt.show()


from localization.processing import ImageProcessor
from help_module.img_helper import fast_thermal_image
import cv2

pros = ImageProcessor()
pros.enable_logging()
thermal_data = [103, 104, 105, 107, 106, 106, 106, 107, 107, 107, 107, 104, 105, 106, 106, 107, 105, 106, 107, 107, 106, 107, 105, 106, 106, 105, 105, 105, 105, 102, 101, 102, 105, 105, 104, 105, 106, 106, 106, 106, 107, 106, 105, 105, 107, 106, 104, 106, 105, 105, 105, 106, 106, 105, 105, 105, 104, 105, 105, 104, 104, 101, 100, 101, 108, 107, 105, 107, 103, 105, 105, 107, 105, 106, 106, 106, 106, 106, 105, 106, 106, 105, 104, 106, 104, 106, 104, 103, 104, 105, 103, 105, 103, 102, 101, 102, 107, 105, 106, 102, 106, 105, 105, 105, 106, 105, 105, 105, 107, 105, 106, 105, 105, 106, 105, 103, 104, 105, 104, 104, 104, 105, 104, 103, 104, 100, 103, 101, 107, 106, 104, 105, 106, 105, 106, 108, 105, 106, 105, 105, 105, 105, 106, 106, 105, 105, 105, 105, 105, 106, 106, 104, 102, 105, 103, 104, 98, 103, 103, 100, 105, 106, 105, 104, 106, 106, 105, 106, 106, 106, 106, 106, 106, 106, 104, 106, 105, 105, 105, 105, 106, 105, 105, 105, 104, 104, 103, 102, 100, 101, 101, 101, 106, 106, 106, 106, 105, 106, 106, 107, 106, 107, 105, 105, 107, 106, 106, 107, 106, 105, 106, 106, 106, 105, 105, 104, 104, 104, 104, 102, 101, 99, 100, 100, 104, 103, 105, 105, 105, 107, 106, 107, 107, 107, 106, 106, 107, 105, 106, 106, 107, 106, 105, 105, 105, 104, 104, 106, 103, 105, 104, 103, 99, 99, 100, 99, 103, 105, 106, 106, 106, 108, 106, 107, 107, 107, 106, 107, 107, 107, 106, 107, 106, 106, 105, 106, 107, 105, 104, 105, 104, 104, 104, 103, 101, 99, 101, 101, 105, 105, 106, 106, 106, 106, 105, 106, 107, 106, 106, 106, 106, 107, 106, 106, 107, 106, 106, 105, 105, 104, 106, 105, 104, 103, 104, 102, 101, 99, 99, 100, 104, 106, 106, 107, 106, 107, 106, 108, 108, 106, 107, 106, 107, 107, 106, 107, 106, 107, 106, 106, 106, 106, 106, 105, 104, 106, 104, 104, 101, 100, 96, 99, 105, 105, 107, 106, 107, 106, 106, 107, 107, 107, 107, 108, 107, 106, 106, 105, 107, 106, 106, 105, 105, 105, 105, 106, 105, 104, 104, 104, 103, 100, 98, 99, 106, 106, 106, 107, 107, 106, 107, 108, 107, 107, 107, 107, 107, 106, 107, 108, 107, 107, 106, 106, 106, 107, 106, 106, 105, 105, 103, 105, 103, 102, 103, 97, 106, 106, 107, 106, 107, 106, 108, 107, 107, 107, 107, 107, 107, 106, 107, 107, 108, 107, 105, 106, 107, 107, 105, 106, 105, 105, 104, 104, 103, 102, 102, 101, 106, 106, 106, 107, 107, 107, 107, 108, 108, 108, 111, 109, 107, 108, 107, 107, 107, 108, 107, 107, 105, 106, 106, 106, 105, 105, 104, 105, 104, 105, 104, 104, 108, 106, 106, 107, 108, 107, 107, 109, 108, 114, 107, 121, 108, 109, 107, 107, 107, 107, 106, 106, 107, 105, 106, 105, 106, 106, 105, 105, 107, 108, 105, 103, 106, 108, 105, 107, 108, 107, 108, 110, 114, 120, 137, 119, 127, 112, 109, 110, 115, 117, 114, 111, 107, 107, 107, 106, 105, 107, 103, 108, 109, 107, 104, 103, 105, 107, 108, 107, 107, 108, 109, 109, 119, 121, 131, 137, 124, 119, 109, 112, 126, 127, 123, 118, 108, 107, 107, 106, 106, 106, 104, 104, 105, 103, 105, 105, 106, 107, 109, 109, 108, 109, 111, 112, 113, 122, 131, 135, 127, 124, 111, 113, 129, 133, 124, 119, 109, 108, 109, 111, 108, 110, 106, 106, 107, 109, 107, 108, 106, 113, 108, 109, 109, 109, 112, 111, 117, 117, 130, 123, 127, 122, 111, 112, 128, 131, 119, 115, 110, 110, 110, 112, 112, 110, 112, 112, 110, 106, 106, 105, 115, 108, 111, 109, 108, 108, 110, 112, 115, 118, 133, 135, 124, 125, 115, 117, 124, 122, 119, 119, 113, 112, 119, 129, 122, 117, 112, 114, 112, 107, 106, 109, 108, 113, 107, 107, 108, 110, 110, 111, 114, 116, 131, 134, 124, 121, 116, 114, 122, 122, 121, 120, 113, 113, 118, 125, 119, 117, 110, 111, 109, 106, 104, 105, 110, 109, 109, 110, 107, 111, 111, 112, 113, 114, 118, 122, 120, 119, 115, 114, 119, 125, 124, 121, 116, 116, 117, 119, 122, 122, 113, 113, 110, 110, 105, 108, 106, 108, 107, 109, 109, 108, 109, 112, 112, 114, 115, 117, 118, 117, 117, 118, 119, 121, 121, 119, 118, 116, 118, 122, 127, 124, 115, 115, 109, 113, 106, 110]

pros.set_thermal_data(thermal_data)
img = pros._get_thresh_img()
# pros.save_progress()
# pros.get_imgs()

# cv2.imshow('image', img)
img.show()

cv2.waitKey(0)
