import commands
ips = commands.getoutput("/sbin/ifconfig | grep -i \"inet\" | awk '{print $2}'")
print ips

macs = commands.getoutput("/sbin/ifconfig | grep -i \"HWaddr\" | awk '{print $5}'")
print macs

from uuid import getnode as get_mac
macs2=get_mac()
print macs2   # converts mac to 48 bit integer
