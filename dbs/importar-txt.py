import datetime
import bottle
import mtwsgi
import json
import random
import sqlite3
from bottle import get, post, request
from datetime import datetime, timedelta
from dateutil import parser


conn = sqlite3.connect('db.sqlite', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
cursor = conn.cursor()


id=1
sensors = 5 
date_object = parser.parse('Nov 5 2016  12:00AM')

filename = 'dados.txt'

gateway_id = int(id)
if gateway_id != 1: 
    initial_sensor_id = (gateway_id-1) * sensors + 1
else:
    initial_sensor_id = 1

#cursor.execute("DELETE from publicacoes where gateway_id=?", ( gateway_id))

cursor.execute("DELETE from {tn} where gateway_id= {key}={idf} ".\
            format(tn="publicacoes", key="gateway_id", idf=gateway_id))

# Using the newer with construct to close the file automatically.
with open(filename) as f:
    data = f.readlines()

initial = True
read_date = date_object

for lines in data:
    register = lines.split(' ')
    if initial == False:
        read_date = read_date + timedelta(minutes=1)
    else:
        initial = False 

    last_value = register[2].replace("\n","")
    fValue = float(last_value)
    
    for s in range(1,sensors+1):
        sensorId = initial_sensor_id+s-1
        
        try:
            
            cursor.execute("INSERT INTO publicacoes ( sensor_id, gateway_id, datacoleta, valorcoletado ) VALUES (?, ?, ?, ?)", (sensorId, gateway_id, read_date, fValue))
        
        except sqlite3.IntegrityError:
            print('ERROR: ID already exists in PRIMARY KEY column {}')


conn.commit()
conn.close()
