from PIL import Image, ImageDraw
from scipy.interpolate import griddata
import numpy as np
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import scipy.ndimage.filters as fil

def convert_to_thermal_image(pixels, scale=1, interpolate=False, fixed_range=False, heat_min=10, heat_max=45):
    fig = Figure()
    ax0 = fig.add_subplot(1, 2, 1)
    ax1 = fig.add_subplot(1, 2, 2)

    img_ar = np.array(pixels).reshape((24, 32))
    result = fil.gaussian_filter(img_ar, 1)

    c = ax0.pcolor(img_ar)
    d = ax1.pcolor(result)

    fig.colorbar(c, ax=ax0)
    fig.colorbar(d, ax=ax1)

    ax1.axis('equal')
    ax0.axis('equal')

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)

    return output.getvalue()


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