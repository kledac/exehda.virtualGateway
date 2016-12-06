# exehda.virtualGateway

Para executar utilizar:
python3 main.py

Dbs localizadas na pasta DBS. 
Configuração inicial:
6 zonas de manejo
6 gateway por zona de manejo
5 sensores por gateway
ZN 1
ids: 1-30
ZN 2
ids: 31-60

e assim por diante.

chamada para requisição de um sensor:

http://0.0.0.0:8081/sensor/?uuId=<id>

O programa decide automaticamente qual DB deve escolher para requisitar a informação.

Tempo de leitura está definido no arquivo mtbottle.py na linha 29, atualmente 5 minutos.

O programa, sempre que executado, reinicia os dados publicados, retornando ao estágino inicial, como se nada tivesse sido publicado.
Isso pode ser desativado alterando a variável restart_simulation no arquivo mtbottle.py.
