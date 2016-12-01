import datetime
import bottle
import mtwsgi
import json
import random
import sqlite3
from bottle import get, post, request
from datetime import datetime, timedelta
from dateutil import parser



id=1
sensors = 5 

date_object = parser.parse('Jun 1 2016  12:00AM')

conn = sqlite3.connect('db.sqlite', detect_types=sqlite3.PARSE_DECLTYPES)
cursor = conn.cursor()


gateway_id = int(id)
if gateway_id != 1: 
    initial_sensor_id = (gateway_id-1) * sensors + 1
else:
    initial_sensor_id = 1


cursor.execute("SELECT id, initial_value, steps_to_max, steps_taken, variation_per_step, final_value FROM {tn} where {key}={idf} ".\
            format(tn="gateway", key="id", idf=gateway_id))


for registro in cursor.fetchall():
    initial_value = float(registro[1])
    steps_to_max = int(registro[2])
    steps_taken = int(registro[3])
    variation_per_step = float(registro[4])
    final_value = float(registro[5])
    Y = (final_value - initial_value)
    #print(str(final_value))


for x in range(steps_taken, steps_to_max+1):
    read_date = date_object + timedelta(hours=x/2)
    current_value = (x/steps_to_max)*Y + initial_value
    last_value=0
    string_values=""
    neg=1
    average = 0
    for s in range(0, sensors):
        temp = random.uniform(1,variation_per_step)
        sensorId = initial_sensor_id+s 
        if last_value != 0:
            current_value = (last_value*temp - last_value)
            if neg==2:
                current_value = current_value*-1
                neg=1
            else:
                neg=2
            current_value = current_value + last_value
        last_value = current_value
        #print(str(sensorId))

        try:
            
            cursor.execute("INSERT INTO publicacoes ( sensor_id, gateway_id, datacoleta, valorcoletado ) VALUES (?, ?, ?, ?)", (sensorId, gateway_id, read_date, last_value))
            #cursor.execute("INSERT INTO publicacoes ( sensor_id, gateway_id, datacoleta, valorcoletado) VALUES ({sID}, {gtID}, {cDate}, {vl})".\
             #   format(sID=sensorId, vl=last_value, gtID=gateway_id, cDate=str(read_date)))

        except sqlite3.IntegrityError:
            print('ERROR: ID already exists in PRIMARY KEY column {}')


        average = average + last_value
    
    average = average / sensors

    try:

        cursor.execute("INSERT INTO publicacoes_media ( sensor_id, gateway_id, datacoleta, valorcoletado ) VALUES (?, ?, ?, ?)", (initial_sensor_id, gateway_id, read_date, average))

    except sqlite3.IntegrityError:
        print('ERROR: ID already exists in PRIMARY KEY column {}')


    print(str(read_date) + " Average: " + str(average))
    
    conn.commit()

    

    #json = json + """{"value":"""+" \""+str("%.2f" % round(last_value,2))+"\""+""", "id_sensor":"""+" \""+str(sensor_id)+"\""+""", "id_gateway": """+" \""+str(gateway_id)+"\""+"""}"""

            

                
#conn.commit()


conn.close()
json = ""
