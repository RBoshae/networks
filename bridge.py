# Same as protocol.py

import socket
import sys
from thread import *
import commands         # Used to get Local IP and MAC informtation

ips = commands.getoutput("/sbin/ifconfig | grep -i \"inet\" | awk '{print $2}'")
ips = ips.split("\n")
LOCAL_IP = ips[0][4:]


macs = commands.getoutput("/sbin/ifconfig | grep -i \"HWaddr\" | awk '{print $5}'")
macs = macs.split("\n")
LOCAL_MAC = macs[0][]



from uuid import getnode as get_mac
macs2=get_mac()
print macs2   # converts mac to 48 bit integer


# Ports
PORT_A = 8000
PORT_B = 8001
PORT_C = 8002
PORT_D = 8003

# IPs
IP_A = "10.0.100.1"
IP_B = "10.0.100.2"
IP_C = "10.0.100.3"
IP_D = "10.0.100.4"

# MACs
MAC_A = "08:00:27:26:03:93"
MAC_B = "08:00:27:58:32:0d"
MAC_C = "08:00:27:58:68:98"
MAC_D = "00:24:1d:5c:5b:dc"

# LOCAL info
LOCAL_PORT = ''      # Arbitrary non-privileged port
LOCAL_NODE = ''
LOCAL_IP = ''
LOCAL_MAC = ''

HOST = ''        # Symbolic name meaning all available interfaces


# Requirement 3. Each bridge will have a table with the MAC, port
# number, status where status is either Root Port, Designated Port, of
# Blocked Port. Initially the table is empty with only port numbers but
# when the system is stable, all ports should have the appropriate
# status (RP, BP, or DP).

# an empty internal table with columns for MAC, Port Number and status.
BridgeTable = []

# Requirement 10
def printBridgeTable():
	print(BridgeTable)



def main(Bridge):
	global LOCAL_PORT       # Arbitrary non-privileged port
	global LOCAL_NODE
	global LOCAL_IP
	global LOCAL_MAC

	# Ports
	PORT1 = 8001
	PORT2 = 8002
	PORT3 = 8003

	# Setup Default Bridge table (MAC, Portn No, Port Status)
	BridgeTable.append([LOCAL_MAC],[PORT1],["DP"])
	BridgeTable.append([LOCAL_MAC],[PORT2],["DP"])
	BridgeTable.append([LOCAL_MAC],[PORT3],["DP"])


	# Binds local socket to port to make sure that (this) is listening for traffic.
	Port1_to_Bridge = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print 'Port 1 to Bridge Socket created.'

	Port2_to_Bridge = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print 'Port 2 to Bridge Socket created.'

	Port3_to_Bridge = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print 'Port 3 to Bridge Socket created.'

	#To avoid port reuse problem, the function below is used
	Port1_to_Bridge.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	Port2_to_Bridge.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	Port3_to_Bridge.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	try:
		Port1_to_Bridge.bind((HOST, PORT1))
		Port2_to_Bridge.bind((HOST, PORT2))
		Port3_to_Bridge.bind((HOST, PORT3))
	except socket.error , msg:
		print 'Bridges Bind failed. Error Code: ' + str(msg[0]) + ' Message ' + msg[1]
		sys.exit()

	print 'Bridge to Ports Socket bind complete'

	Port1_to_Bridge.listen(10)
	print 'Port1 to Bridge Socket now listening'

	Port2_to_Bridge.listen(10)
	print 'Port2 to Bridge Socket now listening'

	Port3_to_Bridge.listen(10)
	print 'Port3 to Bridge Socket now listening'

	#now keep talking with the client
	while 1:
		#wait to accept a connection - blocking call
		conn1, addr1 = Port1_to_Bridge.accept()
		print 'Connected with ' + addr1[0] + ':' + str(addr1[1])

		conn2, addr2 = Port2_to_Bridge.accept()
		print 'Connected with ' + addr2[0] + ':' + str(addr2[1])

		conn3, addr3 = Port3_to_Bridge.accept()
		print 'Connected with ' + addr3[0] + ':' + str(addr3[1])

		#start new thread takes 1st argument as a function name to be run, second is the tuple arguments
		start_new_thread(clientthread, (conn1,))
		start_new_thread(clientthread, (conn2,))
		start_new_thread(clientthread, (conn3,))

	Port1_to_Bridge.close()
	Port2_to_Bridge.close()
	Port3_to_Bridge.close()


if __name__ == '__main__':
	if len(sys.argv) < 2:
		print("python Bridge.py")
		quit(1)
	main(sys.argv[1])
