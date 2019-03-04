import time
import datetime

date_conv = '%Y-%m-%d %H:%M:%S.%f%z'

def convert_to_datetime(input):
    time_string = input[:-3] + input[-2:]
    return datetime.datetime.strptime(time_string, date_conv)


def meas_to_time(meas):
    return str(meas.timestamp).split(".")[0]

if __name__ == "__main__":
    s1 = '2019-02-28 15:00:39.749340+01:00'
    s2 = '2019-02-28 15:00:39.749680+01:00'

    t1 = convert_to_datetime(s1)
    t2 = convert_to_datetime(s2)

    print((t2 - t1).microseconds)