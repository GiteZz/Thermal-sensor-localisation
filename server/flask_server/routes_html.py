from flask import render_template, url_for, flash, redirect, request, jsonify
from flask_server import app, db
from flask_server.models import *
from help_module.webcam_helper import get_values

@app.route("/debug_screen")
def get_debug_screen():
    return render_template('debug.html')

@app.route("/view/stream_test")
def get_test_stream_screen():
    return render_template('test_stream.html')

@app.route("/socketio_test")
def get_socketio_test():
    return render_template('test_socketio.html')

@app.route("/main")
def get_main():
    return render_template('main.html')

@app.route('/config/webcams')
def config_webcams():
    current_webcams = get_values()
    return render_template('webcam_information.html', current_webcams=current_webcams)