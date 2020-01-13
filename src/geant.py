#!/usr/bin/python

from topology import GeantTopology
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.node import RemoteController

import signal
import sys

bw = 10

geant_topo = GeantTopology(bw=bw)

net = Mininet(topo=geant_topo, link=TCLink, controller=None, autoSetMacs=True)

print('Configure your controller correctly before starting the simulation...')
print('type <ENTER>')

input()

net.addController('rmController', controller=RemoteController,
                  ip='127.0.0.1', port=6653)
                  
net.start()
CLI(net)
#Gerando trafego pela CLI usando net.pingall() e net.iperf()