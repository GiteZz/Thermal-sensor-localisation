from sqlalchemy import create_engine, Table, MetaData, Column, Integer, String, DateTime, ARRAY
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('postgres://postgres:postgres@localhost:5432/postgres')
connection = engine.connect()


meta = MetaData()
'''
table = Table('thermal_data', meta,
    Column('device_id', Integer, primary_key=True),
    Column('seq_id', Integer),
    Column('time', DateTime, primary_key=True),
    Column('data', ARRAY(Integer)))

meta.create_all(engine)

##
# meta.bind(engine)
# #
#

'''
# Retrieve data from database
print(engine.table_names())
print(engine.execute('SELECT * FROM Sensor_data'))
stmt = 'SELECT * FROM Sensor_data'

results_poxy = connection.execute(stmt)

results = results_poxy.fetchall()
print(results[0])

# Inserting



print(engine.table_names())