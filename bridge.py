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

# Get MAC info from host and store in LOCAL_MAC
macs = commands.getoutput("/sbin/ifconfig | grep -i \"HWaddr\" | awk '{print $5}'")
macs = macs.split("\n")
LOCAL_BRIDGE_MAC = macs[0]

# LOCAL info
BRIDGE_NAME = ''
LOCAL_BRIDGE_IP = ''
LOCAL_BRIDGE_MAC = ''
BRIDGE_ID = LOCAL_BRIDGE_MAC

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
BRIDGE_ONE_IP   = "10.0.0.1"
BRIDGE_TWO_IP   = "10.0.0.2"
BRIDGE_THREE_IP = "10.0.0.3"
BRIDGE_FOUR_IP  = "10.0.0.4"

 # PORT Mapping
BRIDGE_ONE_PORT_MAPPING   = {(BRIDGE_TWO_IP, PORT_THREE), (BRIDGE_THREE_IP, PORT_ONE), (BRIDGE_FOUR_IP ,PORT_TWO)}
BRIDGE_TWO_PORT_MAPPING   = {(BRIDGE_ONE_IP, PORT_THREE), (BRIDGE_THREE_IP,PORT_TWO), (BRIDGE_FOUR_IP, PORT_ONE)}
BRIDGE_THREE_PORT_MAPPING = {(BRIDGE_ONE_IP, PORT_TWO), (BRIDGE_TWO_IP,PORT_ONE), (BRIDGE_THREE_IP, PORT_THREE)}

# Set BRIDGE_PORT_MAPPING_LOCAL to designated mapping
if LOCAL_BRIDGE_IP == BRIDGE_ONE_IP:
	BRIDGE_PORT_MAPPING_LOCAL = BRIDGE_ONE_PORT_MAPPING
elif: LOCAL_BRIDGE_IP == BRIDGE_TWO_IP:
	BRIDGE_PORT_MAPPING_LOCAL = BRIDGE_TWO_PORT_MAPPING
elif: LOCAL_BRIDGE_IP == BRIDGE_THREE_IP:
	BRIDGE_PORT_MAPPING_LOCAL = BRIDGE_THREE_PORT_MAPPING
elif: LOCAL_BRIDGE_IP == BRIDGE_FOUR_IP:
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


# Root Bridge - Default value of bridge
root_bridge = True

# Used to track time for send_bpdu
five_seconds_passed = True

# Requirement 10
def printBridgeTable():
	print(Bridge_Table)

# Help method called by setup_bridge.
def send_bpdu():
	global five_seconds_passed
	global Bridge_Table
	global BRIDGE_ONE_IP
	global BRIDGE_ONE_PORT_MAPPING
	global BRIDGE_TWO_PORT_MAPPING
	global BRIDGE_THREE_PORT_MAPPING
	global root_bridge
	print 'Broadcasting BPDU'
	five_seconds_passed = True

	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	# Define what will be sent in the BPDU. Store the value in message.
	Y =				# Y is the bridge ID of the node that the sending bridge thinks is the root,
	d = DISTANCE	# d is the cost to reach Y
	X =				# X is the bridge ID of the bridge sending the message.
	bpdu_message =

	if LOCAL_BRIDGE_IP == BRIDGE_ONE_IP:
		for rowEntry in Bridge_Table:
			if rowEntry[2] == "DP":
				if rowEntry == 1:
					s.sendto("msg", (BRIDGE_ONE_PORT_MAPPING[0][0], BRIDGE_ONE_PORT_MAPPING[0][1]) )
				elif rowEntry == 2:
					s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
					s.sendto("msg", (BRIDGE_ONE_PORT_MAPPING[1][0], BRIDGE_ONE_PORT_MAPPING[1][1]) )
				elif rowEntry == 3:
					s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
					s.sendto("msg", (BRIDGE_ONE_PORT_MAPPING[2][0], BRIDGE_ONE_PORT_MAPPING[2][1]) )
				else:
					root_bridge = False
					print "Settled"

	if LOCAL_BRIDGE_IP == BRIDGE_TWO_IP:
		for rowEntry in Bridge_Table:
			if rowEntry[2] == "DP":
				if rowEntry == 1:
					s.sendto("msg", (BRIDGE_TWO_PORT_MAPPING[0][0], BRIDGE_TWO_PORT_MAPPING[0][1]) )
				elif rowEntry == 2:
					s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
					s.sendto("msg", (BRIDGE_TWO_PORT_MAPPING[1][0], BRIDGE_TWO_PORT_MAPPING[1][1]) )
				elif rowEntry == 3:
					s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
					s.sendto("msg", (BRIDGE_TWO_PORT_MAPPING[2][0], BRIDGE_TWO_PORT_MAPPING[2][1]) )
				else:
					root_bridge = False
					print "Settled"

	if LOCAL_BRIDGE_IP == BRIDGE_THREE_IP:
		for rowEntry in Bridge_Table:
			if rowEntry[2] == "DP":
				if rowEntry == 1:
					s.sendto("msg", (BRIDGE_THREE_PORT_MAPPING[0][0], BRIDGE_THREE_PORT_MAPPING[0][1]) )
				elif rowEntry == 2:
					s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
					s.sendto("msg", (BRIDGE_THREE_PORT_MAPPING[1][0], BRIDGE_THREE_PORT_MAPPING[1][1]) )
				elif rowEntry == 3:
					s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
					s.sendto("msg", (BRIDGE_THREE_PORT_MAPPING[2][0], BRIDGE_THREE_PORT_MAPPING[2][1]) )
				else:
					root_bridge = False
					print "Settled"

	if LOCAL_BRIDGE_IP == BRIDGE_FOUR_IP:
		for rowEntry in Bridge_Table:
			if rowEntry[2] == "DP":
				if rowEntry == 1:
					s.sendto("msg", (BRIDGE_FOUR_PORT_MAPPING[0][0], BRIDGE_FOUR_PORT_MAPPING[0][1]) )
				elif rowEntry == 2:
					s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
					s.sendto("msg", (BRIDGE_FOUR_PORT_MAPPING[1][0], BRIDGE_FOUR_PORT_MAPPING[1][1]) )
				elif rowEntry == 3:
					s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
					s.sendto("msg", (BRIDGE_FOUR_PORT_MAPPING[2][0], BRIDGE_FOUR_PORT_MAPPING[2][1]) )
				else:
					root_bridge = False
					print "Settled"

#Function for handling connections. This will be used to create threads
def clientthread(conn):
	global Bridge_Table
	print 'received BPDU from '

	for rowEntry in Bridge_Table:
		Bridge_Table[1] = "BP"
	#inifinte loop so that function do not terminate and thread do not end
	while True:

		#Receiving from client
		data = conn.recv(1024)

		reply = 'OK...' + data

		# Use split to parse data. First parameter is delimeter. Second parameter is number of cuts.
		user_input = data.split(" ", 3)

		# Various flags
		quit_string = '!q'
		forward_string = '!fw'
		forward_report_string = data[0:7]

		# Print ARPTable flag
		ARP = 'arp'
		PRINT_ARP_TABLE = '-a'

		if (user_input[0] == ARP) and (user_input[1] == PRINT_ARP_TABLE):
			printArpTable();

		#Adding pingmac
		USER_INPUT_PINGMAC = 'pingmac'

		if user_input[0] == USER_INPUT_PINGMAC:
			pingmac(user_input)

		if user_input[0] == quit_string:
			break
		if not data:
			break
		if forward_report_string == '!report':
			print 'Printing Report:'
			print (forwardReport[:][:])
		if user_input[0] == forward_string:
			print 'Preparing to forward to server'

			forwarder_to_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			print 'Forwarder to Server Socket created.'

			# use split to parse input
			user_input = data.split(" ", 3)
			# Get host from string
			host = user_input[1]
			print 'host is: ' + host

			port = user_input[2]
			print 'port is: ' + port

			message = user_input[3]
			print 'message: ' + message

			try:
				remote_ip = socket.gethostbyname( host )
			except socket.gaierror:
				# could not resolve
				print 'Hostname could not be resolved. Exiting'
				sys.exit()

			# Connect to remote server
			forwarder_to_server.connect((remote_ip, int(port)))

			forwarder_to_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

			print 'Socket Connected to ' + host + ' on ip ' + remote_ip
			forwarder_to_server.sendall(user_input[3])
			print 'Message sent to server'

			# record message details to forwardReport
			# Specifically, it needs to keep the folloowing:
                        #   the client info:
			#      source IP and source port
                        #   server info:
                        #      destination IP and destination port
                        #   message

			forwardReport.append([str(addr[0]),str(addr[1]),remote_ip,user_input[2],user_input[3]])

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

	# Ports
	global PORT_ONE
	global PORT_TWO
	global PORT_THREE

	# Port Bridge Map
	global BRIDGE_ONE_PORT_MAPPING
	global BRIDGE_TWO_PORT_MAPPING
	global BRIDGE_THREE_PORT_MAPPING

	# Determine whether bridge is root or not.
	global root_bridge
	global five_seconds_passed

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
	while 1:

		if(root_bridge and five_seconds_passed):
			five_seconds_passed = False
			threading.Timer(5.0,send_bpdu).start()



if __name__ == '__main__':
	if len(sys.argv) > 1:
		print("python Bridge.py")
		quit(1)
	setup_bridge(LOCAL_BRIDGE_IP)
