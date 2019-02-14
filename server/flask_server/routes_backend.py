from flask import render_template, url_for, flash, redirect, request
from flask_server import app, db
from flask_server.models import Measurement
import json


@app.route('/sensor/debug', methods=['POST'])
def receive_sensor_debug():
    data = request.json
    new_db_data = Measurement(sensor_id=data["device_id"], data=data["data"], sequence_id=data["sequence"])
    db.session.add(new_db_data)
    db.session.commit()
    return "Hello World!"