from PIL import Image, ImageDraw
from scipy.interpolate import griddata
import numpy

def convert_to_thermal_image(width, height, pixels, scale=1, interpolate=False):
    img = Image.new('RGB', (width, height))
    d = ImageDraw.Draw(img)

    heat_min = min(pixels)
    heat_max = max(pixels) - heat_min

    red_pixels = [int(((pixel - heat_min) / heat_max)*255) for pixel in pixels]

    for x in range(width):
        for y in range(height):
            d.point((x,y), fill=(red_pixels[x + y * width], 0, 255 - red_pixels[x + y * width]))

    if interpolate:
        img = img.resize((width * scale, height * scale), resample=Image.BICUBIC)
    else:
        img = img.resize((width * scale, height * scale))

    return img