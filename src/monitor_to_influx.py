import requests
import time
import datetime
from influxdb import InfluxDBClient
import math
import signal
import sys
import pandas as pd

BASE_URL_API = 'http://localhost:8181/onos/v1'

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
        self.db_client.create_database('onos_utilization')
        self.username = 'onos'
        self.password = 'rocks'
        self.df = pd.read_csv('/home/mj/Documentos/Git Lab repositories/Version_control_backup/Git/arbitrium/logs/utilization.csv')

    def read_csv(self):
        print(df)

if __name__ == '__main__':
     monitor = APIMonitor()
     monitor.read_csv()
#     while(True):
#         time.sleep(20)
#         monitor.get_stats()