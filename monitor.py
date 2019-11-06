import requests
import time
import datetime
from influxdb import InfluxDBClient
import math
import signal
import sys

from config import ONOS_IP, ONOS_PORT

BASE_URL_API = 'http://{0}:{1}/onos/v1'.format(ONOS_IP, ONOS_PORT)

#BASE_URL_API = 'http://localhost:8181/onos/v1'

class APIMonitor(object):
    def __init__(self):        
        #Cria e conecta ao cliente Onos settando:
        #     Host: ip address where InfluxDB is installed
        #     Port: 8086
        #     Username: onos
        #     Password: onos.password (rocks/onos)
        #InfluxDBClient(host, port, user, password, dbname
        self.db_client = InfluxDBClient('localhost', 8086, 'onos', 'rocks', 'onos') 
        
        #Cria o banco de dados
        self.db_client.create_database('onos')
        self.username = 'onos'
        self.password = 'rocks'

    def get_stats(self):
        res = requests.get(
            BASE_URL_API + '/statistics/delta/ports',
            auth=(self.username, self.password)
        )

        data = res.json()
 
        for stats in data['statistics']:
            json_body = {
                "measurement": "utilization",
                "tags": {
                    "device": stats["device"],
                },
                "time": datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
                "fields": {
                    "value": 0
                }
            }

            for stat in stats['ports']:
                json_body["fields"]["value"] = json_body["fields"]["value"] + \
                                               math.ceil(stat["bytesReceived"]/stat["durationSec"])
                json_body["fields"]["value"] = json_body["fields"]["value"] + \
                                               math.ceil(stat["bytesSent"]/stat["durationSec"])

            json_body = [json_body, ]
            self.db_client.write_points(json_body, time_precision='ms')


def signal_handler(signal, frame):
    sys.exit(0)

if __name__ == '__main__':
    monitor = APIMonitor()
    while(True):
        time.sleep(20)
        print('Sending...')
        monitor.get_stats()
        signal.signal(signal.SIGINT, signal_handler)