#!/usr/bin/python

from mininet.node import Host,OVSSwitch,Controller
from mininet.link import Link

b1 = Host ( 'b1' )
b2 = Host ( 'b2' )
b3 = Host ( 'b3' )
b4 = Host ( 'b4' )
s1 = OVSSwitch( 's1', inNamespace=False )
c0 = Controller( 'c0', inNamespace=False )
Link( b1, s1 )
Link( b2, s1 )
Link( b3, s1 )
Link( b4, s1 )

b1.setIP( '10.0.0.1/24' )
b1.setMAC('00.00.00.00.00.00')
b2.setIP( '10.0.0.2/24' )
b3.setIP( '10.0.0.3/24' )
b4.setIP( '10.0.0.4/24' )
c0.start()
s1.start( [c0] )

print b1.IP
print b2.IP
print b3.IP
print b4.IP
# print 'Pinging...'
# print b1.cmd('ping -c3 ', b2.IP() )
# print b1.cmd('ping -c3', b3.IP() )
# s1.stop()
# c0.stop()
