from flask import Flask
import json
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
from os.path import dirname
from localization.server_bridge import ServerBridge

postgres_user = '??'
postgres_pass = '??'

with open(r'C:\Users\Thomas\Documents\School\VOP\VOP\server\configuration_files\db_configuration.json', 'r') as f:
    data = json.load(f)

postgres_user = data['postgres']['username']
postgres_pass = data['postgres']['password']
postgres_db = data['postgres']['db_name']

app_path = dirname(__file__)
VOP_path = dirname(dirname(app_path))
template_path = VOP_path + '/GUI/html_templates'
static_path = VOP_path + '/GUI/static'

app = Flask(__name__, template_folder=template_path, static_folder=static_path)
# app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgres://{postgres_user}:{postgres_pass}@localhost:5432/{postgres_db}'
db = SQLAlchemy(app)
socketio = SocketIO(app)
loc_bridge = ServerBridge()


from flask_server import routes_backend
from flask_server import routes_frontend
from flask_server import routes_html
from flask_server import routes_io