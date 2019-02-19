from flask_server import app, db, socketio

@socketio.on('connect')
def say_hello():
    print("Hellllooooo!!!!")