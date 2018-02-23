import socket
import sys
from thread import *

HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8000 # Arbitrary non-privileged port

#Added Node Parameters for Lab 7
LOCAL_NODE = "A"
LOCAL_IP = "10.0.100.2"
LOCAL_MAC = "08:00:28:26:03:93"

# an empty internal ARP table with columns for IP address, MAC and time-to-live.
ARPTable = [] 


clientList = []
forwardReport = []

client_to_forwarder = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Client to Forwarder Socket created.'


#forwarder_to_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#print 'Forwarder to Server Socket created.'

#To avoid port reuse problem, the function below is used
client_to_forwarder.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#forwarder_to_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try: 
	client_to_forwarder.bind((HOST, PORT))
except socket.error , msg:
	print 'Forwarder Bind failed. Error Code: ' + str(msg[0]) + ' Message ' + msg[1]
	sys.exit()
print 'Forwarder Socket bind complete'

client_to_forwarder.listen(10)
print 'Forwarder Socket now listening'

#Function for handling connections. This will be used to create threads
def clientthread(conn):
	#Sending message to connected client
	conn.send('Welcome to the Forwarder A. Type something and hit enter\n') #send only takes string

	#inifinte loop so that function do not terminate and thread do not end
	while True:
		
		#Receiving from client
		data = conn.recv(1024)
	
		reply = 'OK...' + data

		# Use split to parse data. First parameter is delimeter. Second parameter is number of cuts.
		commands = data.split(" ", 3)
		
		# Various flags
		quit_string = '!q'
		forward_string = '!fw'
		forward_report_string = data[0:7]
		
		#Adding pingmac
		pingmac_command = 'pingmac'

		if commands[0] == pingmac_command:
			print 'Pinging ' + commands[1]
			doesNotExistInARPTable = true			

			# Check local arp table
			for ip in ARPTable:
				if ip[0] == commands[1]:
					
					# Set value to true if found in ARP Table
					doesNotExistInARPTable = false
					
					# Send Message to IP
					print 'IP exists in ARPTable. Sending Message.'
					break
				else:
					# Send broadcast to check for IP
					print 'IP not in ARPTable. Broadcasting to find it.'
					# create a socket
			
			if doesNotExistInARPTable:
				# LEFT OFF HERE
			
			
			

		if commands[0] == quit_string:
			break
		if not data:
			break
		if forward_report_string == '!report':
			print 'Printing Report:'
			print (forwardReport[:][:])
		if commands[0] == forward_string:
			print 'Preparing to forward to server'

			
			forwarder_to_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			print 'Forwarder to Server Socket created.'
			
			# use split to parse input
			command = data.split(" ", 3)
			# Get host from string
			host = command[1]
			print 'host is: ' + host

			port = command [2]
			print 'port is: ' + port 

			message = command[3]
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
			forwarder_to_server.sendall(command[3])
			print 'Message sent to server'

			# record message details to forwardReport
			# Specifically, it needs to keep the folloowing:
                        #   the client info: 
			#      source IP and source port
                        #   server info:
                        #      destination IP and destination port
                        #   message
	
			forwardReport.append([str(addr[0]),str(addr[1]),remote_ip,command[2],command[3]])

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
