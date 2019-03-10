import time
import datetime

date_conv = '%Y-%m-%d %H:%M:%S.%f%z'

def convert_to_datetime(input):
    time_string = input[:-3] + input[-2:]
    return datetime.datetime.strptime(time_string, date_conv)


def meas_to_time(meas):
    return str(meas.timestamp).split(".")[0]


# time1 - time2
def clean_diff(time1, time2):
    if time1 > time2:
        diff = time1 - time2
    else:
        diff = time2 - time1

    sec_diff = diff.days * 24 * 60 * 60 + diff.seconds + diff.microseconds * 0.000001

    if time2 > time1:
        return -1 * sec_diff
    else:
        return sec_diff


if __name__ == "__main__":
    s1 = '2019-02-28 15:00:39.749340+01:00'
    s2 = '2019-02-28 15:00:39.749680+01:00'

    t1 = convert_to_datetime(s1)
    t2 = convert_to_datetime(s2)

    print(clean_diff(t1,t2))