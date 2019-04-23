import csv
from localization.processing import ImageProcessor
from help_module.time_helper import convert_to_datetime, get_time_str
from PIL import Image, ImageDraw
import os

pros = ImageProcessor()
data_list = []

folder_location = '../../data/'
file_name = 'bad_frames.csv'

timestamp_top_margin = 20

file_without_ext = file_name.split('.')[0]
video_folder_name = 'video_' + file_without_ext + '/'

if not os.path.exists(folder_location + video_folder_name):
    os.mkdir(folder_location + video_folder_name)

with open(folder_location + file_name) as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for index, row in enumerate(reader):
        print(row)
        thermal_data = eval(row[0])
        pros.set_thermal_data(thermal_data)
        meas_datetime = convert_to_datetime(row[1])
        local_time = get_time_str(meas_datetime, microseconds=True, seconds=True)

        centroid_frame = Image.fromarray(pros.plot_centroids(rgb=True), 'RGB')

        raw_data = Image.fromarray(pros.get_scaled_img(rgb=True), 'RGB')

        img_width = centroid_frame.size[0]
        img_height = centroid_frame.size[1]
        comp = Image.new('RGB', (img_width, img_height + timestamp_top_margin))

        d = ImageDraw.Draw(comp)
        d.text((0, 0), local_time, fill=(255, 255, 255))

        comp.paste(centroid_frame, (0, 20))
        comp.save(folder_location + video_folder_name + f'{str(index).zfill(5)}.png')

        comp.paste(raw_data, (0, 20))
        comp.save(folder_location + video_folder_name + f'{str(index).zfill(5)}.png')

# ffmpeg -r 12 -f image2 -s 1920x1080 -i %05d.png -vcodec libx264 -crf 10  -pix_fmt yuv420p test.mp4