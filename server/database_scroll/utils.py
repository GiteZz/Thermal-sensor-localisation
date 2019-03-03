import time
import datetime

date_conv = '%Y-%I-%d %H:%M:%S %z'

def convert_to_datetime(input):
    time_string = input[:19] + ' ' + input[-6:].replace(':', '')
    return datetime.datetime.strptime(time_string, date_conv)
