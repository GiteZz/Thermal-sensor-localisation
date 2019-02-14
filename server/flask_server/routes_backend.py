from flask import render_template, url_for, flash, redirect, request
from flask_server import app
from flask_server.models import *

@app.route('/sensor/debug', methods = ['POST'])
def receive_sensor_debug():
    data = request.json
    print(data)
    return "Hello World!"