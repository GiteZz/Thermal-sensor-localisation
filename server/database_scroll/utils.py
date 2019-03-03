import time
import datetime

date_conv = '%Y-%m-%d %H:%M:%S.%f%z'

def convert_to_datetime(input):
    time_string = input[:-3] + input[-2:]
    return datetime.datetime.strptime(time_string, date_conv)


if __name__ == "__main__":
    s1 = '2019-02-28 15:00:37.575494+01:00'
    s2 = '2019-02-28 15:00:39.494231+01:00'
    s3 = '2019-02-28 15:00:39.749340+01:00'

    t1 = convert_to_datetime(s1)
    t2 = convert_to_datetime(s2)
    t3 = convert_to_datetime(s3)

    d1 = (t2 - t1).seconds
    d2 = t3 - t2
    d3 = t3 - t1

    a = 5