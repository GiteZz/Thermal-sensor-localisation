import requests
import random
import time

width = 32
height = 24

test_amount = 40
device_amount = 1

sequence_array = [0] * device_amount

POST_url = 'http://192.168.1.112:5000/sensor/debug'

for _ in range(test_amount):
    time.sleep(0.1)
    thermal_image = [random.randrange(0,100) for _ in range(width * height)]
    device_id = random.randrange(0,device_amount)
    sequence_array[device_id] += 1

    json_dict = {'device_id': device_id, 'sequence': sequence_array[device_id], 'data': thermal_image}

    r = requests.post(POST_url, json=json_dict)
    print(r.status_code)