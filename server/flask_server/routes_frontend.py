from flask import render_template, url_for, flash, redirect, request, jsonify
from flask_server import app, db
from flask_server.models import *

from help_module.img_helper import convert_to_thermal_image
from help_module.flask_helper import serve_pil_image

@app.route("/")
def home():
    return "Hello World!"

@app.route("/thermal_data/images", methods=['GET'])
def get_last_thermal_image():
    scaled_up = request.args.get('scale_up')
    scaled_up = 1 if scaled_up is None else int(scaled_up)

    interpolate = request.args.get('interpolate')
    interpolate = True if interpolate == "1" else False

    print(scaled_up, interpolate)
    last_result = Measurement.query.order_by(Measurement.timestamp.desc()).first()
    img = convert_to_thermal_image(32, 24, last_result.data, scale=scaled_up, interpolate=interpolate)

    print(f'Retrieved image from: {last_result.timestamp}')

    return serve_pil_image(img)

@app.route("/thermal_sensor/amount", methods=['GET'])
def count_sensors():
    amount = Measurement.query.distinct(Measurement.sensor_id).count()
    print(amount)
    return str(amount)

@app.route("/thermal_sensor/ids", methods=['GET'])
def get_ids():
    query_list = Measurement.query.distinct(Measurement.sensor_id).all()
    id_list = [meas.sensor_id for meas in query_list]
    return jsonify({"id_list": id_list})

@app.route("/thermal_sensor/<id>/last_image", methods=['GET'])
def get_sensor_last_image(id):
    scaled_up = request.args.get('scale_up')
    scaled_up = 1 if scaled_up is None else int(scaled_up)

    interpolate = request.args.get('interpolate')
    interpolate = True if interpolate == "1" else False
    print(id)
    last_result = Measurement.query.filter(Measurement.sensor_id == int(id)).\
        order_by(Measurement.timestamp.desc()).first()

    img = convert_to_thermal_image(32, 24, last_result.data, scale=scaled_up, interpolate=interpolate)

    return serve_pil_image(img)