from flask import render_template, url_for, flash, redirect
from flask_server import app, db
from flask_server.models import *


@app.route("/")
def home():
    return "Hello World!"

@app.route("/thermal_data/images", methods=['GET'])
def get_last_thermal_image():
    last_result = Measurement.query.order_by(Measurement.timestamp).first()
    print(last_result)
    return "Hello World"