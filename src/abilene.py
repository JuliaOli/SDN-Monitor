#!/usr/bin/python

import os
import shutil
import unittest

from topology import AbileneTopology
#from datacenter.profiles import WeibullProfile
#from datacenter.dc import Datacenter

from mininet.net import Mininet
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.node import RemoteController

from management.monitor import APIMonitor
from management.monitor import MonitoringThread

from tests.imr_tests import TestIMR

bw = 10

topo = AbileneTopology(bw=bw)

tenants = list()
tenants.append(WeibullProfile(num_nodes=10, n_of_iterations=1000))

dc = Datacenter()

net = Mininet(topo=topo,
              link=TCLink,
              controller=None,
              autoSetMacs=True,
              autoStaticArp=True)

dc.setup(net.hosts, tenants)

print('Configure your controller correctly before starting the simulation...')
print('type <ENTER>')

input()

net.addController('rmController', controller=RemoteController,
                  ip='192.168.202.40', port=6633)

net.start()

# Before starting the simulation, run a ping all.
while net.pingAll() > 0:
    continue

# Start the monitoring thread
output = open("./logs/utilization.log", "w+")
monitor = APIMonitor(output)

# Creating the threads
monitoring_thread = MonitoringThread(monitor)

# Before starting the threads, execute the testing.
runner = unittest.TextTestRunner()

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestIMR('test_if_ifwd_is_active'))
    suite.addTest(TestIMR('test_if_imr_is_active'))
    suite.addTest(TestIMR('test_if_imr_get_stats_is_non_empty'))
    return suite


test_result = runner.run(suite())
print("If there are failures in your ONOS setup, please revise it. Then type ENTER[]")
input()

monitoring_thread.start()

for i in range(0, 30):
    print("Running iteration: {0}".format(i))
    dc.start()
    # CLI(net)
    dc.stop()

    source = './logs'
    dest = './results/mc/{0}'.format(i)
    dest_srv = dest + '/server'
    dest_clnt = dest + '/client'

    os.makedirs(dest)
    os.makedirs(dest_srv)
    os.makedirs(dest_clnt)

    files = os.listdir(source)
    for f in files:
        if f.__contains__('server'):
            shutil.move(os.path.join(source, f), dest_srv)
        elif f.__contains__('client'):
            shutil.move(os.path.join(source, f), dest_clnt)

monitoring_thread.stop()
# Wait the thread to finish it
monitoring_thread.join()
output.close()
net.stop()
