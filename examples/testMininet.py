#!/usr/bin/python

from mininet.topo import Topo, SingleSwitchTopo
from mininet.net import Mininet
from mininet.log import lg, info
from mininet.cli import CLI

def main():
    lg.setLogLevel('info')

    net = Mininet(SingleSwitchTopo(k=2))
    net.start()

    h1 = net.get('h1')
    x1 = h1.popen('python testServer.py -i %s &' % h1.IP())

    h2 = net.get('h2')
    h2.cmd('python testClient.py -i %s -m "test message"' % h1.IP())

    CLI( net )
    x1.terminate()
    net.stop()

if __name__ == '__main__':
    main()
