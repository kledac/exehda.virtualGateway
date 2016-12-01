import requests
import json
#import urllib2
import urllib.request


url = "http://127.0.0.1:8081/"
data = {"id":1,"uuID":"123e4567-e89b-12d3-a456-426655440030","model":"v1","gateway":1,"manufacturer":1,"sensorType":2}
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
r = requests.post(url, data=json.dumps(data), headers=headers)

#req = urllib.request.Request('http://127.0.0.1:8081/')
#req.add_header('Content-Type', 'application/json')

#response = urllib2.urlopen(req, json.dumps(data))
#url = 'http://127.0.0.1:8081/'

#payload = {"id":1,"uuID":"123e4567-e89b-12d3-a456-426655440030","model":"v1","gateway":1,"manufacturer":1,"sensorType":2}

#r = requests.post(req, json.dumps(payload))
