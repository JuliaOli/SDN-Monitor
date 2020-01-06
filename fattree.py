import os
import signal
import shutil
import threading
import subprocess
import unittest
import signal

from monitor import APIMonitor

from mininet.net import Mininet
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.node import RemoteController

numEdgeSwitches = 4
hostsPerEdge = 2
bw = 10

fattree = FattreeTopology(numEdgeSwitches=numEdgeSwitches, bw=bw,
                          hostsPerEdge=hostsPerEdge)

def keyboardInterruptHandler(signal, frame):
    print("KeyboardInterrupt (ID: {1}) has been caught. Cleaning up...".format(signal))
    net.stop()
    exit(0)

signal.signal(signal.SIGINT, keyboardInterruptHandler)

print('Configure your controller correctly before starting the simulation...')
print('type <ENTER>')

input()

net.addController('rmController', controller=RemoteController,
                  ip='127.0.0.1', port=6653)

net.start()

# Before starting the simulation, run a ping all.
while net.pingAll() > 0:
    continue

# Start the monitoring thread
# output = open("./logs/utilization.log", "w+")

# # Creating the threads
# monitoring_thread = MonitoringThread(monitor, output)

# # Before starting the threads, execute the testing.
# runner = unittest.TextTestRunner()

# def suite():
#     suite = unittest.TestSuite()
#     suite.addTest(TestIMR('test_if_ifwd_is_active'))
#     suite.addTest(TestIMR('test_if_imr_is_active'))
#     suite.addTest(TestIMR('test_if_imr_get_stats_is_non_empty'))
#     return suite

# test_result = runner.run(suite())
# print("If there are failures in your ONOS setup, please revise it. Then type ENTER[]")
# input()

# monitoring_thread.start()
# for i in range(1, 30):
#     print("Running iteration: {0}".format(i))
#     dc.start()
#     # CLI(net)
#     dc.stop()

#     # TODO: Move the files from logs to results...
#     source = './logs'
#     dest = './results/mc/{0}'.format(i)
#     dest_srv = dest + '/server'
#     dest_clnt = dest + '/client'

#     os.makedirs(dest)
#     os.makedirs(dest_srv)
#     os.makedirs(dest_clnt)

#     files = os.listdir(source)
#     for f in files:
#         if f.__contains__('server'):
#             shutil.move(os.path.join(source, f), dest_srv)
#         elif f.__contains__('client'):
#             shutil.move(os.path.join(source, f), dest_clnt)

# monitoring_thread.stop()
# # Wait the thread to finish it
# monitoring_thread.join()
# output.close()

monitor = APIMonitor()
while(True):
        time.sleep(20)
        monitor.get_stats()

