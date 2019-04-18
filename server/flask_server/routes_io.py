from flask_server import socketio

@socketio.on('connect')
def say_hello():
    print("Hellllooooo!!!!")