import urllib
params = urllib.urlencode({'spam': 1, 'eggs': 2, 'bacon': 0})


f = urllib.urlopen("http://127.0.0.1:8081/new", params)

#print f.read()
