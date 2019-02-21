from flask import render_template, url_for, flash, redirect, request, jsonify
from flask_server import app, db, socketio
from flask_server.models import Measurement
import json


@app.route('/sensor/debug', methods=['POST'])
def receive_sensor_debug():
    data = request.json
    new_db_data = Measurement(sensor_id=data["device_id"], data=data["data"], sequence_id=data["sequence"], data_type=0)
    db.session.add(new_db_data)
    db.session.commit()
    print(data)
    socketio.emit('new_image', {'device_id': data['device_id']})

    print('NEW post request')

    return "Hello World!"

@app.route('/sensor/bits', methods=['POST'])
def receive_sensor_bits():
    data = request.json
    new_db_data = Measurement(sensor_id=data["device_id"], data=data["data"], sequence_id=data["sequence"], data_type=1)
    db.session.add(new_db_data)
    db.session.commit()
    print(data)
    socketio.emit('new_image', {'device_id': data['device_id']})

    print('NEW post request')

    return "Hello World!"


@app.route('/test/cbor', methods=['POST'])
def test_cbor():
    print("============== CBOR Test ================")
    data = request.json
    print(data)

@app.route('/data/last', methods=['GET'])
def send_data():
    last_result = Measurement.query.order_by(Measurement.timestamp.desc()).first()
    ret_json = {"data":last_result.data, "time":last_result.timestamp, "sensor_id": last_result.sensor_id}
    print(last_result)
    return jsonify(ret_json)