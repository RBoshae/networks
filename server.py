# server.py

import socket
import sys
from thread import *

HOST = ''   # Symbolic name meaning all available interfaces
#PORT = 4798  # Arbitrary non-privileged port
PORT = 8888
clientList = []

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

#To avoid port reuse problem, the function below is used
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try: 
	s.bind((HOST, PORT))
except socket.error , msg:
	print 'Bind failed. Error Code: ' + str(msg[0]) + ' Message ' + msg[1]
	sys.exit()
print 'Socket bind complete'

s.listen(10)
print 'Socket now listening'

#Function for handling connections. This will be used to create threads
def clientthread(conn):
	#Sending message to connected client
	conn.send('Welcome to the server. Type something and hit enter\n') #send only takes string

	#inifinte loop so that function do not terminate and thread do not end
	while True:
		
		#Receiving from client
		data = conn.recv(1024)

		#print recieved data
		print 'Received data from forwarder: ' + data
		break
		#reply = 'OK...' + data

		#data_substring = data[0:2]
		#quit_string = '!q'

		#sendall_string = '!sendall'

		#if data_substring == quit_string:
		#	break
		#if not data:
		#	break
		#if sendall_string == data[0:8]:
		#	for client in clientList:
		#		client.sendall(data[9:1024])
		
		#conn.sendall(reply)
	#came out of loop
	conn.close()
	

#now keep talking with the client
while 1:
	#wait to accept a connection - blocking call
	conn, addr = s.accept()
	clientList.append(conn)
	print 'Connected with ' + addr[0] + ':' + str(addr[1])

	#start new thread takes 1st argument as a function name to be run, second is the tuple arguments
	start_new_thread(clientthread, (conn,))

s.close()
