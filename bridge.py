# Same as protocol.py

import socket
import sys
from thread import *
import commands         # Used to get Local IP and MAC informtation
import threading
import time


# Get IP info from host and store in LOCAL_IP
ips = commands.getoutput("/sbin/ifconfig | grep -i \"inet\" | awk '{print $2}'")
ips = ips.split("\n")
LOCAL_BRIDGE_IP = ips[0][5:]
print 'global ' + LOCAL_BRIDGE_IP

# Get MAC info from host and store in LOCAL_MAC
macs = commands.getoutput("/sbin/ifconfig | grep -i \"HWaddr\" | awk '{print $5}'")
macs = macs.split("\n")
LOCAL_BRIDGE_MAC = macs[0]
print 'global ' + LOCAL_BRIDGE_MAC

# Ports
PORT_ONE = 8001
PORT_TWO = 8002
PORT_THREE = 8003

HOST = ''        # Symbolic name meaning all available interfaces

# BRIDGES
BRIDGE_ONE   = "B1"
BRIDGE_TWO   = "B2"
BRIDGE_THREE = "B3"
BRIDGE_FOUR  = "B4"

# BRIDGE IPs
BRIDGE_ONE_IP   = '10.0.0.1'
BRIDGE_TWO_IP   = '10.0.0.2'
BRIDGE_THREE_IP = '10.0.0.3'
BRIDGE_FOUR_IP  = '10.0.0.4'

 # PORT Mapping
# BRIDGE_ONE_PORT_MAPPING   = {(BRIDGE_TWO_IP, PORT_THREE), (BRIDGE_THREE_IP, PORT_ONE), (BRIDGE_FOUR_IP ,PORT_TWO)}
# BRIDGE_TWO_PORT_MAPPING   = {(BRIDGE_ONE_IP, PORT_THREE), (BRIDGE_THREE_IP,PORT_TWO), (BRIDGE_FOUR_IP, PORT_ONE)}
# BRIDGE_THREE_PORT_MAPPING = {(BRIDGE_ONE_IP, PORT_ONE), (BRIDGE_FOUR_IP,PORT_TWO), (BRIDGE_FOUR_IP, PORT_THREE)}
# BRIDGE_FOUR_PORT_MAPPING = {(BRIDGE_ONE_IP, PORT_TWO), (BRIDGE_TWO_IP,PORT_ONE), (BRIDGE_THREE_IP, PORT_THREE)}
BRIDGE_ONE_PORT_MAPPING   = [[BRIDGE_TWO_IP, PORT_THREE], [BRIDGE_THREE_IP, PORT_ONE], [BRIDGE_FOUR_IP ,PORT_TWO]]
BRIDGE_TWO_PORT_MAPPING   = [[BRIDGE_ONE_IP, PORT_THREE], [BRIDGE_THREE_IP, PORT_TWO], [BRIDGE_FOUR_IP, PORT_ONE]]
BRIDGE_THREE_PORT_MAPPING = [[BRIDGE_ONE_IP, PORT_ONE], [BRIDGE_FOUR_IP, PORT_TWO], [BRIDGE_FOUR_IP, PORT_THREE]]
BRIDGE_FOUR_PORT_MAPPING = [[BRIDGE_ONE_IP, PORT_TWO], [BRIDGE_TWO_IP, PORT_ONE], [BRIDGE_THREE_IP, PORT_THREE]]

# Set BRIDGE_PORT_MAPPING_LOCAL to designated mapping
if LOCAL_BRIDGE_IP == BRIDGE_ONE_IP:
	BRIDGE_PORT_MAPPING_LOCAL = BRIDGE_ONE_PORT_MAPPING
elif LOCAL_BRIDGE_IP == BRIDGE_TWO_IP:
	BRIDGE_PORT_MAPPING_LOCAL = BRIDGE_TWO_PORT_MAPPING
elif LOCAL_BRIDGE_IP == BRIDGE_THREE_IP:
	BRIDGE_PORT_MAPPING_LOCAL = BRIDGE_THREE_PORT_MAPPING
elif LOCAL_BRIDGE_IP == BRIDGE_FOUR_IP:
	BRIDGE_PORT_MAPPING_LOCAL = BRIDGE_FOUR_PORT_MAPPING
else:
	print 'Count not assign port mapping. Line 54'

# Requirement 3. Each bridge will have a table with the MAC, port
# number, status where status is either Root Port, Designated Port, of
# Blocked Port. Initially the table is empty with only port numbers but
# when the system is stable, all ports should have the appropriate
# status (RP, BP, or DP).

# an empty internal table with columns for MAC, Port Number and status.
Bridge_Table = []

# LOCAL info
BRIDGE_NAME = ''
LOCAL_BRIDGE_IP = ''
BRIDGE_ID = LOCAL_BRIDGE_MAC
# Root Bridge - Default value of bridge
DISTANCE_FROM_ROOT = 0
ROOT_BRIDGE_ID = BRIDGE_ID

# Debugging
MESSAGE_NUMBER = 0

# Requirement 10
def printBridgeTable():
	global ROOT_BRIDGE_ID
	global BRIDGE_ID
	global MESSAGE_NUMBER

	MESSAGE_NUMBER = MESSAGE_NUMBER + 1

	print 'Message ' + str(MESSAGE_NUMBER)

	if (ROOT_BRIDGE_ID == BRIDGE_ID):
		print 'Root Node'
	else:
		print 'Forwarding Node'

	print(Bridge_Table[0])
	print(Bridge_Table[1])
	print(Bridge_Table[2])

# Help method called by setup_bridge.
def send_bpdu():
	global Bridge_Table
	global ROOT_BRIDGE_ID
	global DISTANCE_FROM_ROOT
	global BRIDGE_ID
	global BRIDGE_PORT_MAPPING_LOCAL

	print 'Broadcasting BPDU'
	printBridgeTable()

	# Outgoing socket
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	print 'Outgoing Socket Created' ## Debugging

	# Define what will be sent in the BPDU. Store the value in message.
	Y =	ROOT_BRIDGE_ID	 			# Y is the bridge ID of the node that the sending bridge thinks is the root,
	d = DISTANCE_FROM_ROOT	 	 	# d is the cost to reach Y
	X =	BRIDGE_ID	 	 			# X is the bridge ID of the bridge sending the message.
	bpdu_message = str(Y) + ' ' + str(d) + ' ' + str(X)

	for rowEntry in Bridge_Table:
		if rowEntry[2] == "DP":
			if rowEntry == Bridge_Table[0]:
				print 'bpdu data'
				print 'msg ' + bpdu_message
				print 'Sending Port ' + str(BRIDGE_PORT_MAPPING_LOCAL[0][1])
				print 'IP: ' + BRIDGE_PORT_MAPPING_LOCAL[0][0]
				print 'Root Port ' + str(BRIDGE_PORT_MAPPING_LOCAL[0][1])

				# Reminder BRIDGE_ONE_PORT_MAPPING   = {(BRIDGE_TWO_IP, PORT_THREE), (BRIDGE_THREE_IP, PORT_ONE), (BRIDGE_FOUR_IP ,PORT_TWO)}
				s.sendto(bpdu_message + ' ' + str(BRIDGE_PORT_MAPPING_LOCAL[0][1]) , ( BRIDGE_PORT_MAPPING_LOCAL[0][0], int(BRIDGE_PORT_MAPPING_LOCAL[0][1]) ) )  #(msg, ip, port)
			elif rowEntry == Bridge_Table[1]:
				s.sendto(bpdu_message + ' ' + str(BRIDGE_PORT_MAPPING_LOCAL[1][1]), (BRIDGE_PORT_MAPPING_LOCAL[1][0], int(BRIDGE_PORT_MAPPING_LOCAL[1][1])))
			elif rowEntry == Bridge_Table[2]:
				s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
				s.sendto(bpdu_message + ' ' + str(BRIDGE_PORT_MAPPING_LOCAL[2][1]), (BRIDGE_PORT_MAPPING_LOCAL[2][0], int(BRIDGE_PORT_MAPPING_LOCAL[2][1])))
			else:
				'No DP\'s'
	s.close() # close socket
	if (ROOT_BRIDGE_ID == BRIDGE_ID):
		threading.Timer(5.0,send_bpdu).start()

def isRootBridge(other_bridge_id, local_bridge):
	obi = other_bridge_id.splt(":")
	lb = local_bridge.splt(":")

	if obi[0] < lb[0]:
		return True
	elif obi[1] < lb[1]:
		return True
	elif obi[2] < lb[2]:
		return True
	elif obi[3] < lb[3]:
		return True
	elif obi[4] < lb[4]:
		return True
	elif obi[5] < lb[5]:
		return True
	else:
		return False

#Function for handling connections. This will be used to create threads
def clientthread(conn):
	global Bridge_Table
	global ROOT_BRIDGE_ID
	global DISTANCE_FROM_ROOT
	global BRIDGE_ID
	print 'received BPDU from ' + addr[0]

	#inifinte loop so that function do not terminate and thread do not end
	while True:

		#Receiving from client
		data = conn.recv(1024)

		# Use split to parse data. First parameter is delimeter. Second parameter is number of cuts.
		user_input = data.split(":")

		Y = user_input[0]
		d = user_input[1]
		X = user_input[2]
		port = int(user_input[3])

		if Y != ROOT_BRIDGE_ID:
			if isRootBridge(Y, ROOT_BRIDGE_ID):
				ROOT_BRIDGE_ID = Y
				DISTANCE_FROM_ROOT = d + 1
				# Change Bridge Table
				for rowEntry in Bridge_Table:
					if Bridge_Table[1] == port:
						Bridge_Table[2] = "RP"
			else:
				# Change Bridge Table
				for rowEntry in Bridge_Table:
					if Bridge_Table[1] == port:
						Bridge_Table[2] = "BP"

		else:
			if d < DISTANCE_FROM_ROOT:
				ROOT_BRIDGE_ID = Y
				# Change Bridge Table
				for rowEntry in Bridge_Table:
					if Bridge_Table[1] == port:
						Bridge_Table[2] = "RP"
			else:
				# Change Bridge Table
				for rowEntry in Bridge_Table:
					if Bridge_Table[1] == port:
						Bridge_Table[2] = "BP"
		if BRIDGE_ID != ROOT_BRIDGE_ID:
			send_bpdu()

	#came out of loop
	conn.close()

def accept_connections_on_port_one(Port1_to_Bridge):
	while 1:
		#wait to accept a connection - blocking call
		conn1, addr1 = Port1_to_Bridge.accept()
		print 'Connected with ' + addr1[0] + ':' + str(addr1[1])

		#start new thread takes 1st argument as a function name to be run, second is the tuple arguments
		start_new_thread(clientthread, (conn1,))

	Port1_to_Bridge.close()


def accept_connections_on_port_two(Port2_to_Bridge):
	while 1:
		conn2, addr2 = Port2_to_Bridge.accept()
		print 'Connected with ' + addr2[0] + ':' + str(addr2[1])

		start_new_thread(clientthread, (conn2,))
	Port2_to_Bridge.close()

def accept_connections_on_port_three(Port3_to_Bridge):
	while 1:
		conn3, addr3 = Port3_to_Bridge.accept()
		print 'Connected with ' + addr3[0] + ':' + str(addr3[1])
		start_new_thread(clientthread, (conn3,))
	Port3_to_Bridge.close()


# setup_bridge identifies the bridge's ip and begins to setting up the
# required connections based on the required port map.


def setup_bridge(Bridge_IP):
	global LOCAL_PORT       # Arbitrary non-privileged port
	global LOCAL_NODE
	global LOCAL_BRIDGE_IP
	global LOCAL_BRIDGE_MAC

	print 'Local' + LOCAL_BRIDGE_MAC # Debugging

	# Ports
	global PORT_ONE
	global PORT_TWO
	global PORT_THREE

	# Setup Default Bridge table (MAC, Portn No, Port Status)
	# All ports are labeled DP because they are Broadcasting
	Bridge_Table.append([LOCAL_BRIDGE_MAC, PORT_ONE, "DP"])
	Bridge_Table.append([LOCAL_BRIDGE_MAC, PORT_TWO, "DP"])
	Bridge_Table.append([LOCAL_BRIDGE_MAC, PORT_THREE, "DP"])

	# Requirement 7 Print each Bridge table state.
	print Bridge_Table

	# Declare Ports and set up socket type
	Port1_to_Bridge = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print 'Port 1 to Bridge Socket created.'
	Port2_to_Bridge = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print 'Port 2 to Bridge Socket created.'
	Port3_to_Bridge = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print 'Port 3 to Bridge Socket created.'

	# To avoid port reuse problem, the function below is used
	Port1_to_Bridge.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	Port2_to_Bridge.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	Port3_to_Bridge.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	# Binds local socket to port to make sure that (this) is listening for traffic.
	try:
		Port1_to_Bridge.bind((HOST, PORT_ONE))
		Port2_to_Bridge.bind((HOST, PORT_TWO))
		Port3_to_Bridge.bind((HOST, PORT_THREE))
	except socket.error , msg:
		print LOCAL_BRIDGE_IP + 'Bridges Bind failed. Error Code: ' + str(msg[0]) + ' Message ' + msg[1]
		sys.exit()

	print 'Bridge to Ports Socket bind complete'

	Port1_to_Bridge.listen(10)
	print 'Port1 to Bridge Socket now listening'

	Port2_to_Bridge.listen(10)
	print 'Port2 to Bridge Socket now listening'

	Port3_to_Bridge.listen(10)
	print 'Port3 to Bridge Socket now listening'

	start_new_thread(accept_connections_on_port_one, (Port1_to_Bridge,))
	start_new_thread(accept_connections_on_port_two, (Port2_to_Bridge,))
	start_new_thread(accept_connections_on_port_three, (Port3_to_Bridge,))

	print 'Starting algorithm in 10 seconds'
	time.sleep(10)

	#now keep talking with the client
	threading.Timer(5.0,send_bpdu).start()



if __name__ == '__main__':
	if len(sys.argv) > 1:
		print("python Bridge.py")
		quit(1)
	setup_bridge(LOCAL_BRIDGE_IP)
