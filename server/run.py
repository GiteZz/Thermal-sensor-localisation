from flask_server import app, socketio

if __name__ == '__main__':
    socketio.run(app, debug=True, host='192.168.1.133')