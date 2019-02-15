import numpy as np
from PIL import Image
import math
from scipy.interpolate import griddata


scale_factor = 20
width = 32
height = 24

points = [(i % width, math.floor(i / width)) for i in range(0, width * height)]
red = np.random.randint(0, 255, (width * height))

grid_x, grid_y = np.mgrid[0:width - 1:(width * 5)*1j, 0:height - 1:(height * 5)*1j]

bicubic = griddata(points, red, (grid_x, grid_y), method='cubic')


red = np.repeat(red, scale_factor, axis=0)
red = np.repeat(red, scale_factor, axis=1)

green = np.zeros((width * scale_factor, height*scale_factor))
blue = 255 - red

rgb_image = np.zeros((width * scale_factor, height * scale_factor, 3))

rgb_image[..., 0] = red
rgb_image[..., 1] = green
rgb_image[..., 2] = blue


im = Image.fromarray(rgb_image.astype('uint8'))
im.save('test_np.png')