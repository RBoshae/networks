import socket
import sys
from thread import *

HOST = ''        # Symbolic name meaning all available interfaces
LOCAL_PORT = 8000      # Arbitrary non-privileged port

#Added Node Parameters for Lab 7
LOCAL_NODE = "A"
LOCAL_IP = "10.0.100.2"
LOCAL_MAC = "08:00:28:26:03:93"

# an empty internal ARP table with columns for IP address, MAC and time-to-live.
ARPTable = []

# Other ports
PORT_B = 8001
PORT_C = 8002
PORT_D = 8003

clientList = []
forwardReport = []

# Binds local socket to port to make sure that (this) is listening for traffic.
client_to_Node_A = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Client to Node A Socket created.'

#To avoid port reuse problem, the function below is used
client_to_Node_A.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
	client_to_Node_A.bind((HOST, PORT))
except socket.error , msg:
	print 'Node A Bind failed. Error Code: ' + str(msg[0]) + ' Message ' + msg[1]
	sys.exit()

print 'Node A Socket bind complete'

client_to_forwarder.listen(10)
print 'Node A Socket now listening'

# 10. Sending command arp -a from a telnet window on any node should print out the current arp table on that node. Don't forget to ping nodes C and D from A to fille the arp table.
def printArpTable():
	print(ARPTable)

def pingmac(user_input):

	# Flag for a row
	isInARPTable = false

	print 'Pinging ' + user_input[1]

	# Begin by checking local arp table
	for rowEntry in ARPTable:
		if rowEntry[0] == user_input[1]:

			# Set value to true if found in ARP Table
			isInARPTable = true
			print 'IP exists in ARPTable. Sending Message.'

			# Send client Message to IP
			break

	if not isInARPTable:
		print 'IP not in ARPTable. Broadcasting to find it.'
		# Send broadcast to all ports and check for IP
		# Set up socket connection with all other ports.

		# create a sockets
		port_a_to_port_b = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print 'Port A to Port B Socket created.'
		port_a_to_port_c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print 'Port A to Port C Socket created.'
		port_a_to_port_d = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print 'Port A to Port D Socket created.'

		#To avoid port reuse problem, the function below is used
		port_a_to_port_b.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		port_a_to_port_c.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		port_a_to_port_d.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		try:
			port_a_to_port_b.bind((HOST, PORT_B))
			port_a_to_port_c.bind((HOST, PORT_C))
			port_a_to_port_d.bind((HOST, PORT_D))
		except socket.error , msg:
			print 'Forwarder Bind failed. Error Code: ' + str(msg[0]) + ' Message ' + msg[1]
			sys.exit()

		print 'Port A to other ports Socket bind complete'

		client_to_forwarder.listen(10)
		print 'Forwarder Socket now listening'



#Function for handling connections. This will be used to create threads
def clientthread(conn):
	#Sending message to connected client
	conn.send('Welcome to the Node A. Type something and hit enter\n') #send only takes string

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


#now keep talking with the client
while 1:
	#wait to accept a connection - blocking call
	conn, addr = client_to_forwarder.accept()
	clientList.append(conn)
	print 'Connected with ' + addr[0] + ':' + str(addr[1])

	#start new thread takes 1st argument as a function name to be run, second is the tuple arguments
	start_new_thread(clientthread, (conn,))

s.close()
