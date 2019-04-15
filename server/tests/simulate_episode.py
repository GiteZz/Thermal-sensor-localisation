import threading
import requests
import random

from help_module.csv_helper import load_csv

def create_timing_list(data, random_id=False, amount_id=1):
    timing_list = []

    add_dict = {}

    index_list = list(range(amount_id))
    index_id = 0

    add_dict['data'] = list(data[0].data)
    if random_id:
        index_id = (index_id + 1) % amount_id
        add_dict['device_id'] = f'sim_{index_list[index_id]}'
    else:
        add_dict['device_id'] = str(data[0].sensor_id)
    add_dict['sequence'] = str(data[0].sequence_id)
    time_diff = 0

    timing_list.append([time_diff, add_dict])

    for index in range(1, len(data)):
        add_dict = {}
        if random_id:
            index_id = (index_id + 1) % amount_id
            add_dict['device_id'] = f'sim_{index_list[index_id]}'
        else:
            add_dict['device_id'] = str(data[index].sensor_id)
        add_dict['data'] = data[index].data
        add_dict['sequence'] = data[index].sequence_id
        time_diff = (data[index].timestamp - data[index - 1].timestamp).microseconds / 1000000

        timing_list.append((time_diff, add_dict))

    return timing_list

def send_request(timer_list, url, speed_up):
    if len(timer_list) > 0:
        json_data = timer_list.pop(0)[1]
        next_time = speed_up * timer_list[0][0]
        print(next_time)
        timer = threading.Timer(next_time, send_request, [timer_list, url, speed_up])
        timer.start()

        r = requests.post(url, json=json_data)
        print(r.status_code)




if __name__ == "__main__":
    csv_folder = '../database_scroll/csv/'
    csv_file = "sensor_data_episode_20190228-150037_51.csv"
    POST_url = "http://localhost:5000/sensor/simulate"

    amount_sensors = 6

    speed_up = 1/amount_sensors

    csv_data = load_csv('51.csv', to_numpy=False)

    timing_list = create_timing_list(csv_data, random_id=True, amount_id=amount_sensors)

    timer = threading.Timer(0, send_request, [timing_list, POST_url, speed_up])
    timer.start()
    print("exit")