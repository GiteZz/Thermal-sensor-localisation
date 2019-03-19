from PIL import Image, ImageDraw
from scipy.interpolate import griddata
import numpy as np
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import scipy.ndimage.filters as fil
from cv2 import *
from datetime import datetime
import time
from help_module.csv_helper import read_data
from help_module.img_processing_helper import ImageProcessor

import math

def raw_color_plot(pixels, to_pil=True):
    fig = Figure()
    ax0 = fig.add_subplot(1,1,1)
    img_ar = np.array(pixels).reshape((24, 32))

    c = ax0.pcolor(img_ar)
    fig.colorbar(c, ax=ax0)

    ax0.axis('equal')

    if to_pil:
        return plt_fig_to_PIL(fig)
    else:
        return fig


def blur_color_plot(pixels, to_pil=True):
    fig = Figure()
    ax0 = fig.add_subplot(1, 1, 1)
    img_ar = np.array(pixels).reshape((24, 32))
    result = fil.gaussian_filter(img_ar, 1)

    c = ax0.pcolor(result)
    fig.colorbar(c, ax=ax0)

    ax0.axis('equal')

    if to_pil:
        return plt_fig_to_PIL(fig)
    else:
        return fig

def hist_plot(pixels, blur=True, to_pil=True):
    fig = Figure()
    ax0 = fig.add_subplot(1, 1, 1)
    img_ar = np.array(pixels).reshape((24, 32))
    if blur:
        img_ar = fil.gaussian_filter(img_ar, 1)

    data = img_ar.reshape((1, -1)).ravel()

    ax0.hist(data, bins=20)

    if to_pil:
        return plt_fig_to_PIL(fig)
    else:
        return fig

def processed_color_plot(pixels,to_pil=True,thresh_method=None, mtplotlib=True):
    '''
    this function processes a raw image
    :param pixels: raw sensor data
    :param to_pil:
    :param thresh_method: which method to use for processing (in Img_processor class)
    :return: a figure on which all objects have a centroid and a contour
    '''
    processor=ImageProcessor()
    if thresh_method:
        processor.set_treshold_method(thresh_method)
    processor.process(pixels)
    data=processor.plot_frame()
    if mtplotlib:
        fig = Figure()
        ax0 = fig.add_subplot(1, 1, 1)
        ax0.imshow(data,origin="lower")
        if to_pil:
            return plt_fig_to_PIL(fig)
        else:
            return fig
    else:
        return Image.fromarray(data, 'RGB') #already rescaled in the processing functions




def plt_fig_to_PIL(fig):
    buf = plt_fig_to_png_bytes(fig)
    img = Image.open(buf)
    return img


# getvalue for streaming
def plt_fig_to_png_bytes(fig):
    buf = io.BytesIO()
    FigureCanvas(fig).print_png(buf)
    buf.seek(0)
    return buf



def fast_thermal_image(pixels, scale=10, smooth=False, side=True):
    """
    Return PIL image with a heatmap of the pixels, this should be faster then a matplotlib plot,
    There are only 9 different colorbrackets
    :param pixels:
    :param scale:
    :param smooth:
    :return:
    """
    img_ar = np.array(pixels).reshape((24,32))

    if smooth:
        img_ar = fil.gaussian_filter(img_ar, 1)

    # nan gets converted to 0
    min_img = np.min(img_ar[img_ar != 0])
    max_img = np.max(img_ar)

    amount_delta = 8
    delta = (max_img - min_img) / amount_delta
    colors = ((0,0,0),(68,1,84),(70,50,126),(54,92,141),(39,127,142),(31,161,135),(74,193,109),(160,218,57),(253,231,37))

    deltas = [min_img]

    for i in range(amount_delta - 1):
        deltas.append(min_img + (i+1) * delta)

    deltas.append(float("inf"))
    if side:
        rgb_img = np.zeros((24, 32+15, 3), dtype=np.uint8)
    else:
        rgb_img = np.zeros((24, 32, 3), dtype=np.uint8)

    for x in range(24):
        for y in range(32):
            for index, color_range in enumerate(deltas):
                pixel_value = img_ar[x,y]
                if img_ar[x,y] < color_range:
                    rgb_img[x,y] = colors[index]
                    break

    rgb_img = rgb_img.repeat(scale, axis=0)
    rgb_img = rgb_img.repeat(scale, axis=1)

    img = Image.fromarray(rgb_img, 'RGB')

    if not side:
        return img

    d = ImageDraw.Draw(img)

    x_sq_start = 32 * scale + 10
    x_sq_stop = x_sq_start + 50
    color_square_height = (24 * scale) / (amount_delta + 1)

    for i in range(1, amount_delta):
        color_text = f'{deltas[i-1]}-{deltas[i]}'
        d.rectangle([(x_sq_start, i*color_square_height), (x_sq_stop, (i + 1)*color_square_height)], fill=colors[i])
        d.text((x_sq_stop + 10, i*color_square_height), color_text, fill=(255,255,255))

    color_text = f'-inf-{deltas[0]}'
    d.text((x_sq_stop + 10, 0), color_text, fill=(255, 255, 255))

    color_text = f'{deltas[-2]}-inf'
    d.rectangle([(x_sq_start, amount_delta * color_square_height), (x_sq_stop, (amount_delta + 1) * color_square_height)], fill=colors[-1])
    d.text((x_sq_stop + 10, amount_delta * color_square_height), color_text, fill=(255, 255, 255))

    return img



def bits_to_thermal_image(width, height, pixels, scale=1, interpolate=False, fixed_range=True, heat_min=10, heat_max=45):
    img = Image.new('RGB', (width, height))
    d = ImageDraw.Draw(img)

    for x in range(width):
        for y in range(height):
            d.point((x,y), fill=(pixels[x + y * width]*255, pixels[x + y * width]*255, pixels[x + y * width]*255))

    if interpolate:
        img = img.resize((width * scale, height * scale), resample=Image.BICUBIC)
    else:
        img = img.resize((width * scale, height * scale))

    return img

def create_timed_image():
    time_str = datetime.now().strftime('%Y%m%d%H%M%S%f%z')

    # initialize the camera
    cam = VideoCapture(1)  # 0 -> index of camera
    s, img = cam.read()
    time.sleep(0.1)
    imwrite('images/' + time_str + ".jpg", img)

def test_speed(data, function):
    t0 = time.time()
    for meas in data:
        function(meas.data)
    t1 = time.time()

    total = t1 - t0
    print(total)


def PIL_to_bytes(img):
    img_io = io.BytesIO()
    img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return img_io.getvalue()

def get_grid_form(amount):
    plot_sizes = [1, 2, 4, 6, 9]
    grid_sizes = [[1, 1], [2, 1], [2, 2], [3, 2], [3, 3]]
    grid = grid_sizes[0]

    for index in range(len(grid_sizes)):
        if amount <= plot_sizes[index]:
            grid = grid_sizes[index]
            break

    return grid

def combine_imgs(img_list, title=None):
    min_width = float('inf')
    for img in img_list:
        if img.size[0] < min_width:
            min_width = img.size[0]

    rescaled_imgs = []
    total_height = 0
    for img in img_list:
        width, height = img.size
        factor = min_width / width
        new_height = int(factor * height)
        rescaled_imgs.append(img.resize((min_width, new_height)))
        total_height += new_height

    comp = Image.new('RGB', (min_width, total_height))
    current_height = 0

    for img in rescaled_imgs:
        comp.paste(img, (0,current_height))
        current_height += img.size[1]

    return comp


if __name__ == "__main__":
    result = read_data("sensor_data_episode_20190221-143435_0.csv")
    frame = result[30][0]
    raw_color_plot(frame).show()

    processed_color_plot(frame).show()

    # fast_thermal_image(result[0].data)
    # test_speed(result[0:100], fast_thermal_image)
    # test_speed(result[0:100], convert_to_thermal_image)