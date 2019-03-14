from flask import render_template, url_for, flash, redirect, request, jsonify
from flask_server import app, db, socketio
from flask_server.models import Measurement, Measurement_test
import cbor2
import json
import math
from help_module.img_helper import create_timed_image

img_refresh = 10
img_index = 0

@app.route('/sensor/debug', methods=['POST'])
def receive_sensor_debug():
    print('NEW post request')
    data = request.json
    print(data)

    data['data'] = [0 if math.isnan(a) else a for a in data['data']]
    print(data)

    new_db_data = Measurement(sensor_id=data["device_id"], data=data["data"], sequence_id=data["sequence"], data_type=0)
    db.session.add(new_db_data)
    db.session.commit()

    socketio.emit('new_image', {'device_id': data['device_id']})

    global img_index
    img_index = (img_index + 1) % img_refresh

    if img_index == 0:
        create_timed_image()

    return "Hello World!"

@app.route('/sensor/simulate', methods=['POST'])
def receive_simulate():
    # print("Simulated request")
    data = request.json
    new_db_data = Measurement_test(sensor_id=data["device_id"], data=data["data"], sequence_id=data["sequence"], data_type=0)
    db.session.add(new_db_data)
    db.session.commit()
    socketio.emit('new_image', {'device_id': data['device_id']})
    return "Succes"

@app.route('/sensor/bits', methods=['POST'])
def receive_sensor_bits():
    data = request.json
    socketio.emit('new_image', {'device_id': data['device_id']})
    print(data)
    data['data'] = [0 if math.isnan(a) else a for a in data['data']]
    print(data)

    db.session.add(new_db_data)
    db.session.commit()
    print(data)


    print('NEW post request')

    return "Hello World!"


@app.route('/test/cbor', methods=['POST'])
def test_cbor():
    print("============== CBOR Test ================")
    data = request.get_data()
    print(data)
    sensor_data = [int(a) for a in data]
    sensor_id = sensor_data[0]
    seq_id = sensor_data[1]
    thermal_data = sensor_data[2:]

    new_db_data = Measurement(sensor_id=sensor_id, data=thermal_data, sequence_id=seq_id, data_type=0)
    db.session.add(new_db_data)
    db.session.commit()

    socketio.emit('new_image', {'device_id': sensor_id})

    print(" CBOR STOP ")
    return 'Hello'

@app.route('/data/last', methods=['GET'])
def send_data():
    last_result = Measurement.query.order_by(Measurement.timestamp.desc()).first()
    ret_json = {"data":last_result.data, "time":last_result.timestamp, "sensor_id": last_result.sensor_id}
    print(last_result)
    return jsonify(ret_json)