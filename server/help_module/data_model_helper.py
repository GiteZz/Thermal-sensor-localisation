from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ARRAY, DateTime, SmallInteger
from datetime import datetime
import numpy as np
from help_module.time_helper import convert_to_datetime

Base = declarative_base()

class Measurement(Base):
    __tablename__= 'Sensor_data'
    sensor_id = Column('sensor_ID',Integer, primary_key=True,nullable=False)
    data = Column('data', ARRAY(Integer), nullable=False)
    sequence_id = Column('sequence_ID', Integer)
    timestamp = Column('timestamp',DateTime, nullable=False,
                        default=datetime.utcnow,primary_key=True)
    data_type = Column('data_type', SmallInteger)

    def __repr__(self):
        return f'<Measurement :: sensor_id={self.sensor_id}, sequence_id={self.sequence_id}>'

class CSV_Measurement:
    def __init__(self, row):
        self.data = np.array(eval(row[0]))
        self.timestamp = convert_to_datetime(row[1])
        self.sequence_id = int(row[2])
        self.sensor_id = 'csv_' + row[3]

    def set_values(self, sensor_id, data, sequence_id, timestamp, data_type):
        self.sensor_id = sensor_id
        self.data = data
        self.sequence_id = sequence_id
        self.timestamp = timestamp
        self.data_type = data_type
