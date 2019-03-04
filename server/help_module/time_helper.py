import time
import datetime

date_conv = '%Y-%m-%d %H:%M:%S.%f%z'

def convert_to_datetime(input):
    time_string = input[:-3] + input[-2:]
    return datetime.datetime.strptime(time_string, date_conv)


def meas_to_time(meas):
    return str(meas.timestamp).split(".")[0]