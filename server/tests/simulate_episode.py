import threading
import requests
import random

from help_module.csv_helper import load_csv

def create_timing_list(data, random_id=False, amount_id=1):
    """

    :param data:
    :param random_id:
    :param amount_id:
    :return:
    """
    timing_list = []

    add_dict = {}

    index_list = list(range(amount_id))
    index_id = 0

    add_dict['data'] = list(data[0].data)
    if random_id:
        index_id = (index_id + 1) % amount_id
        add_dict['device_id'] = f'sim_{index_list[index_id]}'
    else:
        add_dict['device_id'] = 65
    add_dict['sequence'] = str(data[0].sequence_id)
    time_diff = 0

    timing_list.append([time_diff, add_dict])

    for index in range(1, len(data)):
        add_dict = {}
        # if random_id:
        #     index_id = (index_id + 1) % amount_id
        #     add_dict['device_id'] = f'sim_{index_list[index_id]}'
        # else:
        #     add_dict['device_id'] = str(data[index].sensor_id)
        add_dict['device_id'] = 65
        add_dict['data'] = data[index].data
        add_dict['sequence'] = data[index].sequence_id
        time_diff = (data[index].timestamp - data[index - 1].timestamp).microseconds / 1000000

        timing_list.append((time_diff, add_dict))

    return timing_list

def send_request(timer_list, url, speed_up):
    if len(timer_list) > 0:
        json_data = timer_list.pop(0)[1]
        next_time = speed_up * timer_list[0][0]
        timer = threading.Timer(next_time, send_request, [timer_list, url, speed_up])
        timer.start()

        r = requests.post(url, json=json_data)
        if r.status_code == 200:
            print('OK')
        else:
            print(r.status_code)


if __name__ == "__main__":
    csv_folder = 'data/'
    csv_file = "1person_with_border_noise.csv"
    POST_url = "http://localhost:5000/sensor/simulate_no_save"

    amount_sensors = 1

    speed_up = 1/amount_sensors

    csv_data = load_csv(csv_folder+csv_file, to_numpy=False)

    timing_list = create_timing_list(csv_data, random_id=True, amount_id=amount_sensors)

    timer = threading.Timer(0, send_request, [timing_list, POST_url, speed_up])
    timer.start()
    print("exit")