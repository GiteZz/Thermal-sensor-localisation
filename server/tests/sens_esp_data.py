import requests
import random

width = 32
height = 24

test_amount = 1
device_amount = 5

sequence_array = [0] * device_amount

POST_url = 'http://127.0.0.1:5000/sensor/debug'

for _ in range(test_amount):
    thermal_image = [random.randrange(0,100) for _ in range(width * height)]
    device_id = random.randrange(0,device_amount)
    sequence_array[device_id] += 1

    json_dict = {'device_id': device_id, 'sequence': sequence_array[device_id], 'data': thermal_image}

    r = requests.post(POST_url, json=json_dict)
    r.status_code