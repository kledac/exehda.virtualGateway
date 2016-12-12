import datetime
import bottle
import mtwsgi
import json
import random
import sqlite3
from bottle import get, post, request
from datetime import datetime, timedelta
from dateutil.parser import parse


class MTServer(bottle.ServerAdapter):
   
    zones = 6
    gateways_per_zone = 6
    sensors_per_zone = 5

    def __init__(self):
        app = bottle.Bottle()
        

        # TRUE limpa todas informações de dados publicacos
        restart_simulation = True
        if restart_simulation == True:
            #Valor 0 reseta todos sensores
            MTServer.reset_simulation(0)

        #Tempo de leitura do gateway
        read_time = 5


        #@app.route('/sensor/<name:re:[a-z]||[0-9]+>')
        @app.route('/resetData=<name>')
        def time(name):
            MTServer.reset_simulation(name)
            resetado ="Todos"
            if name != "0":
                resetado = str(name)

            json = """{"status":"Sucesso", "sensores":"""+" \""+resetado+"\""+"""}"""

            return json

        @app.route('/sensor/', method='GET')
        def time():

            sensor_id = request.query["uuId"]
            if sensor_id =="":
                return

            uuId = sensor_id
            sensor_id = sensor_id[-2:]
            
            zoneNumber = str(MTServer.zoneDB(int(sensor_id)))
            conn = sqlite3.connect('dbs/zone'+zoneNumber+'.sqlite', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
            cursor = conn.cursor()

            json = ""

            try:
                # select * from {tn} where publicado = false and {key} = {idf} LIMIT 1
                cursor.execute("select sensor_id, gateway_id, datacoleta, valorcoletado from {tn} where publicado = 'false' and {key} = {idf} LIMIT 1 ".\
                        format(tn="publicacoes", key="sensor_id", idf=sensor_id))

                for registro in cursor.fetchall():
                    data = parse(registro[2])
                    data_final = data + timedelta(minutes=read_time-1)
                    json = """{"value":"""+" \""+str(registro[3])+"\""+""", "id_sensor":"""+" \""+str(registro[0])+"\""+""", "id_gateway": """+" \""+str(registro[1])+"\""+""", "dataColeta": """+" \""+str(registro[2])+"\""+"""}"""
                    #print("Sensor Id: " + str(registro[0]) +" Data: " + str(registro[2]) + "  Valor:"  + str(registro[3]) )
                

                cursor.execute("update publicacoes set publicado = 'true' where publicado = 'false' and sensor_id = ? and datacoleta between ? and ?", (sensor_id, data , data_final ))
                # for registro in cursor.fetchall():
                #     print(registro[2])
                # print(data)
                #atualizar para publicado = true apenas nos registros limitados pelos minutos

                # cursor.execute("update publicacoes set publicado = 'true' where sensor_id = {idf}".\
                #         format(tn="publicacoes", key="sensor_id", idf=name))


                #cursor.execute("INSERT INTO publicacoes ( sensor_id, gateway_id, datacoleta, valorcoletado ) VALUES (?, ?, ?, ?)", (sensorId, gateway_id, read_date, fValue))
        
            except sqlite3.IntegrityError:
                print('ERROR: ID already exists in PRIMARY KEY column {}')
            
            #return 'hello, world 2!\n'

            #teste = """{"value":"18.62", "id_sensor": "123e4567-e89b-12d3-a456-42665544001", "id_gateway": "1"}"""
            
            conn.commit()
            conn.close()

            return json

        @app.route('/generateSensors=<id>&quantity=<quantity>&offset=<offset>')
        def new_sensor(id, quantity, offset):
            conn = sqlite3.connect('db.sqlite')
            c = conn.cursor()
            
            gateway_id = int(id)
            initial_value = float(offset)
            total = int(quantity)

            temp = random.uniform(1,1.25)
            json = ""
            last_value = 0
            final_value = initial_value
            neg = random.randint(1, 2)
            for x  in range(0, total):
                temp = random.uniform(1,1.12)
                if last_value != 0:
                    final_value = (last_value*temp - last_value)
                    if neg==2:
                        final_value = final_value*-1
                        neg=1
                    else:
                        neg=2
                    final_value = final_value + last_value
                last_value = final_value
                
                
            
                # A) Inserts an ID with a specific value in a second column
                try:
                    c.execute("INSERT INTO {tn} ({idf}) VALUES ({gt})".\
                        format(tn="sensores", idf="gateway_id", gt=gateway_id))
                    
                    sensor_id = c.lastrowid

                    c.execute("INSERT INTO publicacoes ( sensor_id, gateway_id, datacoleta, valorcoletado) VALUES ({sID}, {gtID}, datetime(), {vl})".\
                        format(sID=c.lastrowid, vl=last_value, gtID=gateway_id))

                    
                except sqlite3.IntegrityError:
                    print('ERROR: ID already exists in PRIMARY KEY column {}')

                json = json + """{"value":"""+" \""+str("%.2f" % round(last_value,2))+"\""+""", "id_sensor":"""+" \""+str(sensor_id)+"\""+""", "id_gateway": """+" \""+str(gateway_id)+"\""+"""}"""

                
            
            conn.commit()
            
            conn.close()
            #json = """{"value":"""+" \""+id+"\""+""", "id_sensor":"""+" \""+quantity+"\""+""", "id_gateway": "1"}"""

            return json


        @app.route('/processGateway=<id>')
        def process_gateway(id):
            date_object = datetime.strptime('Mar 1 2016  0:00AM', '%b %d %Y %I:%M%p')

            conn = sqlite3.connect('db.sqlite')
            cursor = conn.cursor()


            gateway_id = int(id)
    

            cursor.execute("SELECT id, initial_value, steps_to_max, steps_taken, variation_per_step, final_value FROM {tn} where {key}={idf} ".\
                        format(tn="gateway", key="id", idf=gateway_id))

            
            for registro in cursor.fetchall():
                initial_value = float(registro[1])
                steps_to_max = int(registro[2])
                steps_taken = int(registro[3])
                variation_per_step = float(registro[4])
                final_value = float(registro[5])
                         
            #conn.commit()


            conn.close()
            json = ""

            return json


            

        @app.route('/new/', method='GET')
        def new_item():
            new = request.query["uuId"]
            MTServer.zoneDB(int(new))
            return str(MTServer.zoneDB(int(new)))
           

        @app.route('/json<json:re:[0-9]+>', method='GET')
        def show_json(json):
            ju = request.GET.task.strip()
            print(json)
            print(ju)

        @app.route('/', method='POST')
        def index():
            postdata = request.body.read()
            str_data = postdata.decode('utf-8')
            print("----------------------------------")
            print(str_data)#this goes to log file only, not to client

            print(type(str_data))
            print(str_data[uuID])

            print("----------------------------------")
        app.run(host='0.0.0.0', port=8081, thread_count=3)

    def run(self, handler):
        thread_count = self.options.pop('thread_count', None)
        server = mtwsgi.make_server(self.host, self.port, handler, thread_count, **self.options)
        server.serve_forever()
    
    def reset_simulation(id):
        for zone in range(1, MTServer.zones+1):
            conn = sqlite3.connect('dbs/zone'+str(zone)+'.sqlite', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
            cursor = conn.cursor()

            if id==0:
                cursor.execute("update publicacoes set publicado = 'false' where publicado = 'true' ")
            else:
                cursor.execute("update publicacoes set publicado = 'false' where publicado = 'true' and sensor_id=? ", (id))
            
            conn.commit()
            conn.close()

    def zoneDB(sensor_id):

        

        zone = 1

        sensors_in_zone = MTServer.sensors_per_zone * MTServer.gateways_per_zone

        if sensor_id <= sensors_in_zone:
            zone=1
        else:
            divided = (int)(sensor_id / sensors_in_zone)  + 1
            rest = sensor_id % sensors_in_zone
            if rest == 0:
                divided = divided - 1
            zone = divided

        return zone
