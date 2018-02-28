import socket
import sys
from thread import *

# Ports
PORT_A = 8000
PORT_B = 8001
PORT_C = 8002
PORT_D = 8003

# IPs
IP_A = "10.0.100.2"
IP_B = "10.0.100.3"
IP_C = "10.0.100.4"
IP_D = "10.0.100.5"

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

# an empty internal ARP table with columns for IP address, MAC and time-to-live.
ARPTable = []

# Requirement 10
def printArpTable():
	print(ARPTable)

def pingmac(input):
    #
	# if input == 'received':
	# 	print 'pingmac received'

	if input[2] == ':':
		mac = input
		print 'Pinging ' + mac

		# Ping by MAC Address
		for rowEntry in ARPTable:
			if rowEntry[1] == mac:
				# Setup Socket
				node_x_to_node_y = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				print 'Node ' + LOCAL_NODE + ' to Node ' + rowEntry[0] + ' Socket created.'

				#To avoid port reuse problem, the function below is used
				node_x_to_node_y.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

				# Set remote_ip
				try:
					remote_ip = socket.gethostbyname( 'localhost' )
				except socket.gaierror:
					# could not resolve
					print 'Hostname could not be resolved. Exiting'
					sys.exit()

				# Connect to other nodes
				node_x_to_node_y.connect((remote_ip, rowEntry[3]))

				msg = mac + " " + LOCAL_NODE + " " + str(LOCAL_PORT)

				print msg

				node_x_to_node_y.send(msg)

				node_x_to_node_y.close # Close Socket


				break # Job Done

	elif input[2] == '.':
		ip = input[0:-2]

		# Flag for a row
		isInARPTable = False

		print 'Pinging ' + ip

		# Requirement 3 Begin by checking local arp table
		for rowEntry in ARPTable:
			if rowEntry[1] == ip:

				# Set value to true if found in ARP Table
				isInARPTable = True

				print 'IP exists in ARPTable. Sending Message.'
				pingmac(rowEntry[2])

				# Send client Message to IP
				break


		# Requirement 4
		if not isInARPTable:
			print 'IP not in ARPTable. Broadcasting to find it.'
			# Send broadcast to all ports and check for IP
			# Set up socket connection with all other ports.

			# Setup message
			protocal = "ARP"
			opcode = "1"
			source = LOCAL_MAC
			destination = "FF:FF:FF:FF:FF:FF"
			sender_mac = LOCAL_MAC
			sender_ip = LOCAL_IP
			target_mac = "00:00:00:00:00:00"
			target_ip = ip
			source_node = LOCAL_NODE
			source_port = LOCAL_PORT

			message = protocal + " " + opcode + " " + source + " " + destination + " " + sender_mac + " " + sender_ip + " " + target_mac + " " + target_ip + " " + source_node + " " + str(source_port) + " end"
			#print(message)

			try:
				remote_ip = socket.gethostbyname( 'localhost' )
			except socket.gaierror:
				# could not resolve
				print 'Hostname could not be resolved. Exiting'
				sys.exit()

			portList = [8000, 8001, 8002, 8003]
			for port in portList:

				if port == LOCAL_PORT:
					continue

				# create a sockets
				port_x_to_port_y = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				print 'Port ' + str(LOCAL_PORT) +' to Port ' + str(port)  + ' Socket created.'

				# Set socket options
				# To avoid port reuse problem, the function below is used
				port_x_to_port_y.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


				# Connect to other nodes
				port_x_to_port_y.connect((remote_ip, port))

				# Send ip to all sockets
				port_x_to_port_y.send(message)
				print 'Message sent to Port '

				port_x_to_port_y.close


	else:
		print 'invalid input'

# Requirement 5
def receiveARPRequest(incoming_message):
	global ARPTable
	# print 'Incoming message: '
	# print(incoming_message)
	if incoming_message[7] == LOCAL_IP:
		print 'Received ARP from ' + incoming_message[5] + '...replying'

		if incoming_message[1] == "1":
			print 'opcode 1 - message recieved'

			isInARPTable = False

			# Begin by checking local arp table
			for rowEntry in ARPTable:
				if rowEntry[1] == incoming_message[2]:
					# Set value to true if found in ARP Table
					isInARPTable = True
					print 'IP exists in ARPTable. Sending Response.'
					# Response happens below
					break

			if not isInARPTable:
				print 'IP not in ARPTable. Adding to ARPTable.'
				ARPTable.append([incoming_message[8], incoming_message[2], incoming_message[4], incoming_message[9]])

				print "Node " + incoming_message[8] + " added to ARPTable"

				# print (ARPTable)

			print 'Generating Reply'
			# Setup message
			protocal = "ARP"
			opcode = "2"
			source = LOCAL_MAC
			destination = incoming_message[2]
			sender_mac = LOCAL_MAC
			sender_ip = LOCAL_IP
			target_mac = incoming_message[2]
			target_ip = incoming_message[5]
			source_node = LOCAL_NODE
			source_port = LOCAL_PORT


			message = protocal + " " + opcode + " " + source + " " + destination + " " + sender_mac + " " + sender_ip + " " + target_mac + " " + target_ip + " " + source_node + " " + str(source_port) + " end"

			print 'Sending Reply'

			# Set remote_ip
			try:
				remote_ip = socket.gethostbyname( 'localhost' )
			except socket.gaierror:
				# could not resolve
				print 'Hostname could not be resolved. Exiting'
				sys.exit()

			# create a sockets
			node_x_to_node_y = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			print 'Node '+ LOCAL_NODE + ' to Node '+ incoming_message[8] +  ' Socket created.'

			# Connect to other nodes
			node_x_to_node_y.connect((remote_ip, int(incoming_message[9])))


			#To avoid port reuse problem, the function below is used
			node_x_to_node_y.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

			node_x_to_node_y.send(message)

			node_x_to_node_y.close


		# Requirement 7
		if incoming_message[1] == "2":
			print 'opcode 2 - reply recieved'

			print 'Adding message to ARPTable'

			# Add message to ARPTable
			ARPTable.append([incoming_message[8], incoming_message[2], incoming_message[4],int(incoming_message[9])])

			print 'Message added to ARPTable'
			# print 'Current ARP Table'
			# printArpTable()

			pingmac(incoming_message[2])
	# Requirement 6
	else:
		print 'Received ARP from ' + incoming_message[5] + '...ignoring'

#Function for handling connections. This will be used to create threads
def clientthread(conn):
	#Sending message to connected client
	conn.send('Welcome to Node '+ LOCAL_NODE +'. Type something and hit enter\n') #send only takes string

	#inifinte loop so that function do not terminate and thread do not end
	while True:

		#Receiving from client
		data = conn.recv(1024)

		# Use split to parse data. First parameter is delimeter. Second parameter is number of cuts.
		user_input = data.split(" ")

		# Quit flag
		quit_string = '!q'

		# Print ARPTable flag
		ARP = 'arp'
		PRINT_ARP_TABLE = '-a'

		ARP_REQUEST = "ARP"
		ARP_REQUEST_OPCODE_ZERO = "0"
		ARP_REQUEST_OPCODE_ONE = "1"

		#Adding pingmac flag
		USER_INPUT_PINGMAC = 'pingmac'

		if user_input[0] == USER_INPUT_PINGMAC and user_input[1] == 'received':
			print 'pingmac recieved'

		elif user_input[0] == USER_INPUT_PINGMAC:
			pingmac(user_input[1]) # Paramer is either ip or mac addess

		if user_input[0] == ARP_REQUEST:
			# Reply to ARP_REQUEST
			receiveARPRequest(user_input)

		if user_input[0] == ARP and user_input[1][0:-2] == PRINT_ARP_TABLE:
			print 'Printing ARP Table'
			printArpTable();

		if len(user_input[0]) == 17:
			if LOCAL_MAC == user_input[0]:

				print 'Sending pingmac received'

				# Set remote_ip
				try:
					remote_ip = socket.gethostbyname( 'localhost' )
				except socket.gaierror:
					# could not resolve
					print 'Hostname could not be resolved. Exiting'
					sys.exit()

				# create a socket
				node_x_to_node_y = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				print 'Node '+ LOCAL_NODE + ' to Node '+ user_input[1] +  ' Socket created.'

				# Connect to other nodes
				node_x_to_node_y.connect((remote_ip, int(user_input[2])))


				#To avoid port reuse problem, the function below is used
				node_x_to_node_y.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

				node_x_to_node_y.send('pingmac received')





		if user_input[0] == quit_string:
			break
		if not data:
			break

	#came out of loop
	conn.close()

# def setupSocket(Node):
#
# 	# Binds local socket to port to make sure that (this) is listening for traffic.
# 	client_to_Node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 	print 'Client to Node ' + Node + ' Socket created.'
#
# 	#To avoid port reuse problem, the function below is used
# 	client_to_Node.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


def main(Node):
	global LOCAL_PORT       # Arbitrary non-privileged port
	global LOCAL_NODE
	global LOCAL_IP
	global LOCAL_MAC

	# Set Node Parameters
	if Node == 'A':
		LOCAL_PORT = PORT_A      # Arbitrary non-privileged port
		LOCAL_NODE = Node
		LOCAL_IP = IP_A
		LOCAL_MAC = MAC_A
	elif Node == 'B':
		LOCAL_PORT = PORT_B      # Arbitrary non-privileged port
		LOCAL_NODE = Node
		LOCAL_IP = IP_B
		LOCAL_MAC = MAC_B
	elif Node == 'C':
		LOCAL_PORT = PORT_C      # Arbitrary non-privileged port
		LOCAL_NODE = Node
		LOCAL_IP = IP_C
		LOCAL_MAC = MAC_C
	else:
		LOCAL_PORT = PORT_D      # Arbitrary non-privileged port
		LOCAL_NODE = Node
		LOCAL_IP = IP_D
		LOCAL_MAC = MAC_D

	# Binds local socket to port to make sure that (this) is listening for traffic.
	client_to_Node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print 'Client to ' + LOCAL_NODE + ' Socket created.'

	#To avoid port reuse problem, the function below is used
	client_to_Node.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	try:
		client_to_Node.bind((HOST, LOCAL_PORT))
	except socket.error , msg:
		print 'Node ' + LOCAL_NODE + ' Bind failed. Error Code: ' + str(msg[0]) + ' Message ' + msg[1]
		sys.exit()

	print 'Node '+ LOCAL_NODE +' Socket bind complete'

	client_to_Node.listen(10)
	print 'Node ' + LOCAL_NODE + ' Socket now listening'

	#now keep talking with the client
	while 1:
		#wait to accept a connection - blocking call
		conn, addr = client_to_Node.accept()
		print 'Connected with ' + addr[0] + ':' + str(addr[1])

		#start new thread takes 1st argument as a function name to be run, second is the tuple arguments
		start_new_thread(clientthread, (conn,))

	client_to_Node.close()


if __name__ == '__main__':
	if len(sys.argv) < 2:
		print("python Node.py <A|B|C|D>")
		quit(1)
	main(sys.argv[1])
