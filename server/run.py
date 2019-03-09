from flask_server import app, socketio

run_local = True

if __name__ == '__main__':
    if run_local:
        socketio.run(app, debug=True, host='localhost')
    else:
        socketio.run(app, debug=True, host='localhost')