from flask import render_template, url_for, flash, redirect, request, jsonify
from flask_server import app, db
from flask_server.models import *

@app.route("/debug_screen")
def get_debug_screen():
    return render_template('debug.html')

@app.route("/socketio_test")
def get_socketio_test():
    return render_template('test_socketio.html')