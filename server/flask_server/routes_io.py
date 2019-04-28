from flask_server import socketio
from localization.com_module import ComModule
from localization.server_bridge import ServerBridge

socketio.on_event('connect', ComModule.new_connection)
socketio.on_event('disconnect', ComModule.left_connection)

socketio.on_event('reset_trackers', ServerBridge.reset_trackers)