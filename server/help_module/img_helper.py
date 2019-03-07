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
from help_module.csv_helper import load_csv
import math

def convert_to_thermal_image(pixels, scale=1, interpolate=False, fixed_range=False, heat_min=10, heat_max=45):
    fig = Figure()
    ax0 = fig.add_subplot(2, 2, 1)
    ax1 = fig.add_subplot(2, 2, 2)
    ax2 = fig.add_subplot(2, 2, 3)

    img_ar = np.array(pixels).reshape((24, 32))
    result = fil.gaussian_filter(img_ar, 1)
    gem = np.mean(result)
    img_cap = (result > gem)*1


    c = ax0.pcolor(img_ar)
    d = ax1.pcolor(result)
    e = ax2.pcolor(img_cap)

    fig.colorbar(c, ax=ax0)
    fig.colorbar(d, ax=ax1)
    fig.colorbar(e, ax=ax2)

    ax1.axis('equal')
    ax0.axis('equal')

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)

    return output.getvalue()

def fast_thermal_image(pixels, scale=10, smooth=True):
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

    rgb_img = np.zeros((24, 32+15, 3), dtype=np.uint8)
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

    img_io = io.BytesIO()
    img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return img_io.getvalue()




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


if __name__ == "__main__":
    result = load_csv("frame1.csv")
    # fast_thermal_image(result[0].data)
    test_speed(result[0:100], fast_thermal_image)
    # test_speed(result[0:100], convert_to_thermal_image)