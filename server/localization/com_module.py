from flask_server import socketio
from help_module.img_helper import combine_imgs, PIL_to_64

class ComModule:
    def __init__(self):
        self.amount_connections = 0

    def distribute_imgs(self, id, imgs):
        img = combine_imgs(imgs)
        buf = PIL_to_64(img)
        socketio.emit('new_image', {'id': id, 'img': buf.decode('utf-8')})

    def tracker_update(self, data_dict):
        for key, value in data_dict.items():
            socketio.emit('tracker_update', {'ID': key, 'location': value})

    @socketio.on('connect')
    def new_connection(self):
        self.amount_connections += 1

    @socketio.on('disconnect')
    def left_connection(self):
        self.amount_connections -= 1

    def any_clients(self):
        return self.amount_connections > 0