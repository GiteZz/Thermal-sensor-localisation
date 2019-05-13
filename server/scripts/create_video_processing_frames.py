from help_module.csv_helper import load_csv
from help_module.time_helper import clean_diff, abs_diff, get_time_str
from localization.processing import ImageProcessor
from datetime import datetime, timedelta
import os
import math
from PIL import Image, ImageDraw

def save_video_frames(sensor_id, measurements, FPS=28.84):
    start_time = measurements[0].timestamp
    end_time = measurements[-1].timestamp
    cur_time = start_time

    time_diff = clean_diff(end_time, start_time)
    time_jumps = math.floor(time_diff * FPS)
    time_jump = 1 / FPS

    meas_index = 0

    pros = ImageProcessor()

    for i in range(time_jumps):
        print(i)
        cur_time += timedelta(seconds=time_jump)

        while abs_diff(cur_time, measurements[meas_index].timestamp) > abs_diff(cur_time,
                                                                             measurements[meas_index + 1].timestamp):
            meas_index += 1

        pros.set_thermal_data(measurements[meas_index].data)

        local_time = get_time_str(measurements[meas_index].timestamp, microseconds=True, seconds=True)

        centroid_frame = Image.fromarray(pros.plot_centroids(rgb=True), 'RGB')

        img_width = centroid_frame.size[0]
        img_height = centroid_frame.size[1]
        comp = Image.new('RGB', (img_width, img_height + 20))
        d = ImageDraw.Draw(comp)
        d.text((0, 0), local_time, fill=(255, 255, 255))

        img_name = f'{frame_folder}{sensor_id}_' + ('000000' + str(i))[-6:] + '.png'

        comp.paste(centroid_frame, (0, 20))

        comp.save(img_name)


csv_folder = "../../scenarios/1_person_1_sensor/02/"
csv_file = 'sensor_data.csv'
frame_folder = csv_folder + 'frames/'

if not os.path.exists(frame_folder):
    os.mkdir(frame_folder)

data = load_csv(csv_folder + csv_file, to_numpy=True, split=True, csv_tag=False)

for key, value in data.items():
    save_video_frames(int(key), value)