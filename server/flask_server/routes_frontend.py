from flask import render_template, url_for, flash, redirect
from flask_server import app
from flask_server.models import *

@app.route("/")
def home():
    return "Hello World!"