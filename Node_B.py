import socket
import sys
from thread import *

# Other ports
PORT_A = 8000
PORT_B = 8001
PORT_C = 8002
PORT_D = 8003

HOST = ''                # Symbolic name meaning all available interfaces
LOCAL_PORT = PORT_B      # Arbitrary non-privileged port

#Added Node Parameters for Lab 7
LOCAL_NODE = "B"
LOCAL_IP = "10.0.100.3"
LOCAL_MAC = "08:00:27:58:32:0d"

# an empty internal ARP table with columns for IP address, MAC and time-to-live.
ARPTable = []


# Binds local socket to port to make sure that (this) is listening for traffic.
client_to_Node_B = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Client to Node B Socket created.'

#To avoid port reuse problem, the function below is used
client_to_Node_B.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
	client_to_Node_B.bind((HOST, LOCAL_PORT))
except socket.error , msg:
	print 'Node B Bind failed. Error Code: ' + str(msg[0]) + ' Message ' + msg[1]
	sys.exit()

print 'Node B Socket bind complete'

client_to_Node_B.listen(10)
print 'Node B Socket now listening'

# Added for Lab 7

# Requirement 10
def printArpTable():
	print(ARPTable)

def pingmac(input):

	if len(input) == 17:
		mac_address = input
		# Ping by MAC Address

	else:
		ip = input
		# Flag for a row
		isInARPTable = false

		print 'Pinging ' + ip

		# Requirement 3 Begin by checking local arp table
		for rowEntry in ARPTable:
			if rowEntry[1] == ip:

				# Set value to true if found in ARP Table
				isInARPTable = true

				print 'IP exists in ARPTable. Sending Message.'
				pingmac(rowEntry[3])

				# Send client Message to IP
				break

		# Requirement 4
		if not isInARPTable:
			print 'IP not in ARPTable. Broadcasting to find it.'
			# Send broadcast to all ports and check for IP
			# Set up socket connection with all other ports.

			try:
				remote_ip = socket.gethostbyname( 'localhost' )
			except socket.gaierror:
				# could not resolve
				print 'Hostname could not be resolved. Exiting'
				sys.exit()

			# create a sockets
			port_b_to_port_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			print 'Port B to Port A Socket created.'
			port_b_to_port_c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			print 'Port B to Port C Socket created.'
			port_b_to_port_d = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			print 'Port B to Port D Socket created.'

			# Connect to other nodes
			port_b_to_port_a.connect((remote_ip, PORT_A))
			port_b_to_port_c.connect((remote_ip, PORT_C))
			port_b_to_port_d.connect((remote_ip, PORT_D))


			#To avoid port reuse problem, the function below is used
			port_b_to_port_a.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			port_b_to_port_c.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			port_b_to_port_d.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

			# Setup message
			protocal = "ARP"
			opcode = 1
			source = LOCAL_MAC
			destination = "FF:FF:FF:FF:FF:FF"
			sender_mac = LOCAL_MAC
			sender_ip = LOCAL_IP
			target_mac = "00:00:00:00:00:00"
			target_ip = ip

			message = protocal + " " + opcode + " " + source + " " + destination + " " + sender_mac + " " + sender_ip + " " + target_mac + " " + target_ip

			# Send ip to all sockets
			port_b_to_port_a.send(message)
			port_b_to_port_c.send(message)
			port_c_to_port_d.send(message)

# Requirement 5
def receiveARPRequest(message):

	if message[7] == LOCAL_IP:
		print 'Received ARP from ' + message[5] + '...replying'

		if message[1] == 1:
			print 'opcode 1 - message recieved'

			# Begin by checking local arp table
			for rowEntry in ARPTable:
				if rowEntry[1] == message[2]:
					# Set value to true if found in ARP Table
					isInARPTable = true
					print 'IP exists in ARPTable. Sending Response.'


					break

			if not isInARPTable:
				print 'IP not in ARPTable. Adding to ARPTable.'
				ARPTable.append([message[2],message[4],'Port'])

			print 'Sending Response'


		# Requirement 7
		if message[1] == 2:
			print 'opcode 2 - reply recieved'

			print 'Adding message to ARPTable'

			# Add message to ARPTable
			ARPTable.append(['Node',message[2], message[4],'Port '])

			pingmac(message[2])
	# Requirement 6
	else:
		print 'Received ARP from ' + message[5] + '...ignoring'




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
		user_input = data.split(" ")

		# Print ARPTable flag
		ARP = 'arp'
		PRINT_ARP_TABLE = '-a'

		ARP_REQUEST = "ARP"
		ARP_REQUEST_OPCODE_ZERO = "0"
		ARP_REQUEST_OPCODE_ONE = "1"

		if user_input[0] == ARP_REQUEST:
			# Reply to ARP_REQUEST
			receiveARPRequest(user_input)
			# TODO HERE

		if user_input[0] == ARP and user_input[1] == PRINT_ARP_TABLE:
			printArpTable();

		#Adding pingmac flag
		USER_INPUT_PINGMAC = 'pingmac'

		if user_input[0] == USER_INPUT_PINGMAC:
			pingmac(user_input[1]) # Paramer is either ip or mac addess

		if user_input[0] == quit_string:
			break
		if not data:
			break

	#came out of loop
	conn.close()


#now keep talking with the client
while 1:
	#wait to accept a connection - blocking call
	conn, addr = client_to_Node_B.accept()
	print 'Connected with ' + addr[0] + ':' + str(addr[1])

	#start new thread takes 1st argument as a function name to be run, second is the tuple arguments
	start_new_thread(clientthread, (conn,))

s.close()
