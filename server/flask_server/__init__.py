from flask import Flask
import json
from flask_sqlalchemy import SQLAlchemy

postgres_user = '??'
postgres_pass = '??'

with open('configuration.json', 'r') as f:
    data = json.load(f)

postgres_user = data['postgres']['username']
postgres_pass = data['postgres']['password']
postgres_db = data['postgres']['db_name']


app = Flask(__name__)
# app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgres://{postgres_user}:{postgres_pass}@localhost:5432/{postgres_db}'
db = SQLAlchemy(app)


from flask_server import routes_backend
from flask_server import routes_frontend