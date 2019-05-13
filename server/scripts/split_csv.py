from datetime import datetime
from help_module.csv_helper import load_csv, write_csv_list_frames
from help_module.time_helper import convert_to_datetime

date_conv = '%Y-%m-%d %H:%M:%S.%f%z'

start_time_str = "2019-05-09 12:55:21.000000+02:00"
start_time = convert_to_datetime(start_time_str)
stop_time_str = "2019-05-09 13:00:04.000000+02:00"
stop_time = convert_to_datetime(stop_time_str)
csv_file = "data_0905.csv"

measurements = load_csv(csv_file, to_numpy=True, split=False, csv_tag=False)

needed_values = []

for meas in measurements:
    if start_time <= meas.timestamp <= stop_time:
        needed_values.append(meas)

write_csv_list_frames(needed_values, '1persoon1sensor_0905_03')