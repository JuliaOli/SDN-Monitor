#!/usr/bin/python

from datacenter.topology import GeantTopology
from datacenter.profiles import IperfProfile
from datacenter.profiles import PingProfile
from datacenter.dc import Datacenter

from mininet.net import Mininet
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.node import RemoteController

import signal
import sys

def signal_handler(signal, frame):
    net.stop()
    sys.exit(0)

bw = 10

geant_topo = GeantTopology(bw=bw)

tenants = []
for h in range(0, 31):
    tenants.append(IperfProfile(num_nodes=2, duration=80))
    tenants.append(PingProfile(num_nodes=2, duration=60))

dc = Datacenter()

net = Mininet(topo=geant_topo, link=TCLink, controller=None, autoSetMacs=True)

dc.setup(net.hosts, tenants)

print('Configure your controller correctly before starting the simulation...')
print('type <ENTER>')

input()

net.addController('rmController', controller=RemoteController,
                  ip='127.0.0.1', port=6633)
                  #sudo lsof -i -P -n | grep LISTEN command to find the ports

net.start()
CLI(net)
#Gerando trafego pela CLI
# Before starting the simulation, run a ping all.
""" while net.pingAll() > 0:
    continue

net.iperf()

signal.signal(signal.SIGINT, signal_handler) """