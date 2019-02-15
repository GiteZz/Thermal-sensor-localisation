from flask import render_template, url_for, flash, redirect, request
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
    scaled_up = 1 if scaled_up is None else scaled_up

    interpolate = request.args.get('interpolate')
    interpolate = True if interpolate == 1 else False

    print(scaled_up, interpolate)
    last_result = Measurement.query.order_by(Measurement.timestamp).first()
    img = convert_to_thermal_image(32, 24, last_result.data, )
    return serve_pil_image(img)