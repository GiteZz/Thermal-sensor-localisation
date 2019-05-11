from datetime import datetime
from help_module.csv_helper import load_csv, write_csv_list_frames
from help_module.time_helper import convert_to_datetime
from help_module.csv_helper import load_csv
from help_module.time_helper import clean_diff, abs_diff, get_time_str
from localization.processing import ImageProcessor
from localization.Tracker import Tracker
from localization.localiser import Localiser
from datetime import datetime, timedelta
import os
import math
from PIL import Image, ImageDraw

date_conv = '%Y-%m-%d %H:%M:%S.%f%z'

start_time_str = "2019-05-09 12:55:21.000000+02:00"
start_time = convert_to_datetime(start_time_str)
stop_time_str = "2019-05-09 13:00:04.000000+02:00"
stop_time = convert_to_datetime(stop_time_str)



csv_folder = "../../scenarios/1_person_1_sensor/013"
csv_file = 'sensor_data.csv'
frame_folder = csv_folder + 'frames_tracking/'

if not os.path.exists(frame_folder):
    os.mkdir(frame_folder)

measurements = load_csv(csv_folder + csv_file, to_numpy=True, split=False, csv_tag=False)

start_time = measurements[0].timestamp
end_time = measurements[-1].timestamp
cur_time = start_time


time_diff = clean_diff(end_time, start_time)
time_jumps = 8138
time_jump = time_diff / time_jumps

meas_index = 0

tracker = Tracker()

loc_dict = {}

prev_frame = tracker.get_vis()

rgb_frame_start_index = 11

for i in range(time_jumps):
    print(i)
    cur_time += timedelta(seconds=time_jump)

    # cur_time > measurement
    while clean_diff(measurements[0].timestamp, cur_time) < 0:
        cur_meas = measurements.pop(0)

        if cur_meas.sensor_id not in loc_dict:
            loc_dict[cur_meas.sensor_id] = Localiser(cur_meas.sensor_id)
            loc_dict[cur_meas.sensor_id].set_tracker(tracker)
            loc_dict[cur_meas.sensor_id].calibrate_data()

        loc_dict[cur_meas.sensor_id].update(cur_meas.data, cur_meas.timestamp)

        pros_imgs = []
        for locs in loc_dict.values():
            pros_imgs.append(locs.get_scaled_img((600,480)))


        prev_frame = tracker.get_vis()


    img_name = f'{frame_folder}' + ('000000' + str(i))[-6:] + '.png'

    prev_frame.save(img_name)