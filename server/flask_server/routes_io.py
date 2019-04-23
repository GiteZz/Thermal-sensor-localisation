from flask_server import socketio
from localization.com_module import ComModule

@socketio.on('connect')
def say_hello():
    print("Socketio new client")
    ComModule.new_connection()

@socketio.on('disconnect')
def say_hello():
    print("Socketio left client")
    ComModule.left_connection()