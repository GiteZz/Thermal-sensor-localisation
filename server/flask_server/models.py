from datetime import datetime
from flask_server import db

#this class is created based on the DB relation as defined in db_create.sql
class Measurement(db.Model):
    __tablename__= 'Sensor_data'
    sensor_id=db.Column('sensor_ID',db.Integer, primary_key=True,nullable=False)
    data = db.Column('data', db.Integer, nullable=False)
    sequence_id = db.column('sequence_ID', db.Integer)
    timestamp=db.Column('timestamp',db.DateTime, nullable=False,
                        default=datetime.utcnow,primary_key=True)
    #TODO
    #def __repr__(self):
        #return  string(self.sensor_id) + '::'+ self.sequence_id + '->' + self.data



a=Measurement.query.all()
for i in a:
    print (i.data)
    print(i.timestamp)