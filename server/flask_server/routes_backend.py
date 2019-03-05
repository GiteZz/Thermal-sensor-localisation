from flask import render_template, url_for, flash, redirect, request, jsonify
from flask_server import app, db, socketio
from flask_server.models import Measurement
import cbor2
import json
import math
from help_module.img_helper import create_timed_image

img_refresh = 10
img_index = 0

@app.route('/sensor/debug', methods=['POST'])
def receive_sensor_debug():
    data = request.json

    data['data'] = [0 if math.isnan(a) else a for a in data['data']]
    print(data)
    new_db_data = Measurement(sensor_id=data["device_id"], data=data["data"], sequence_id=data["sequence"], data_type=0)
    db.session.add(new_db_data)
    db.session.commit()
    socketio.emit('new_image', {'device_id': data['device_id']})
    print('NEW post request')
    global img_index
    img_index = (img_index + 1) % img_refresh

    if img_index == 0:
        create_timed_image()

    return "Hello World!"

@app.route('/sensor/simulate', methods=['POST'])
def receive_simulate():
    data = request.json
    print(data)
    socketio.emit('new_image', {'device_id': data['device_id']})
    return "Succes"

@app.route('/sensor/bits', methods=['POST'])
def receive_sensor_bits():
    data = request.json
    print(data)
    data['data'] = [0 if math.isnan(a) else a for a in data['data']]
    print(data)

    db.session.add(new_db_data)
    db.session.commit()
    print(data)
    socketio.emit('new_image', {'device_id': data['device_id']})

    print('NEW post request')

    return "Hello World!"


@app.route('/test/cbor', methods=['POST'])
def test_cbor():
    print("============== CBOR Test ================")
    data = request.data
    hello = cbor2.loads(data)
    print(hello)
    print(data)
    print(" CBOR STOP ")
    return 'Hello'

@app.route('/data/last', methods=['GET'])
def send_data():
    last_result = Measurement.query.order_by(Measurement.timestamp.desc()).first()
    ret_json = {"data":last_result.data, "time":last_result.timestamp, "sensor_id": last_result.sensor_id}
    print(last_result)
    return jsonify(ret_json)