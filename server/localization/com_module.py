from flask_server import socketio
from help_module.img_helper import combine_imgs, PIL_to_64

class ComModule:
    def __init__(self):
        pass

    def distribute_imgs(self, id, imgs):
        img = combine_imgs(imgs)
        buf = PIL_to_64(img)
        socketio.emit('new_image', {'id': id, 'img': buf.decode('utf-8')})

    def tracker_update(self, data):
        print("tracker update")