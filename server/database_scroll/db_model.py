from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ARRAY, DateTime, SmallInteger
from datetime import datetime

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