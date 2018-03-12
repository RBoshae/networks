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
LOCAL_HOST = LOCAL_BRIDGE_IP

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

# ADDED TO MATCH PROJECT
if LOCAL_BRIDGE_IP == BRIDGE_ONE_IP:
	LOCAL_BRIDGE_MAC = "00:00:00:00:00:00"
elif LOCAL_BRIDGE_IP == BRIDGE_TWO_IP:
	LOCAL_BRIDGE_MAC = "01:00:00:00:00:00"
elif LOCAL_BRIDGE_IP == BRIDGE_THREE_IP:
	LOCAL_BRIDGE_MAC = "41:00:00:00:00:00"
elif LOCAL_BRIDGE_IP == BRIDGE_TWO_IP:
	LOCAL_BRIDGE_MAC = "f1:00:00:00:00:00"
else:
	print 'Something went wrong with hardcoding mac'

 # PORT Mapping
BRIDGE_ONE_PORT_MAPPING   = [[BRIDGE_TWO_IP, PORT_THREE], [BRIDGE_THREE_IP, PORT_ONE], [BRIDGE_FOUR_IP ,PORT_TWO]]
BRIDGE_TWO_PORT_MAPPING   = [[BRIDGE_ONE_IP, PORT_THREE], [BRIDGE_THREE_IP, PORT_TWO], [BRIDGE_FOUR_IP, PORT_ONE]]
BRIDGE_THREE_PORT_MAPPING = [[BRIDGE_ONE_IP, PORT_ONE], [BRIDGE_TWO_IP, PORT_TWO], [BRIDGE_FOUR_IP, PORT_THREE]]
BRIDGE_FOUR_PORT_MAPPING = [[BRIDGE_ONE_IP, PORT_TWO], [BRIDGE_TWO_IP, PORT_ONE], [BRIDGE_THREE_IP, PORT_THREE]]

BRIDGE_PORT_MAPPING_LOCAL = []

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
	print 'Could not assign port mapping. Check Line 51'

# Requirement 3. Each bridge will have a table with the MAC, port
# number, status where status is either Root Port, Designated Port, of
# Blocked Port. Initially the table is empty with only port numbers but
# when the system is stable, all ports should have the appropriate
# status (RP, BP, or DP).

# an empty internal table with columns for MAC, Port Number and status.
Bridge_Table = []

# LOCAL info
BRIDGE_NAME = ''
BRIDGE_ID = LOCAL_BRIDGE_MAC
# Root Bridge - Default value of bridge
DISTANCE_FROM_ROOT = 0
ROOT_BRIDGE_ID = BRIDGE_ID

# Debugging
MESSAGE_NUMBER = 0
OUTGOING_MESSAGE_NUMBER = 0

# Requirement 10
def printBridgeTable():
	global ROOT_BRIDGE_ID
	global BRIDGE_ID
	global MESSAGE_NUMBER

	MESSAGE_NUMBER = MESSAGE_NUMBER + 1

	print '\nTable Version: ' + str(MESSAGE_NUMBER)

	if (ROOT_BRIDGE_ID == BRIDGE_ID):
		print 'Root Node'

	print(Bridge_Table[0])
	print(Bridge_Table[1])
	print(Bridge_Table[2])

	return True

# Help method called by setup_bridge.
def sendBPDU(args):
	global Bridge_Table
	global ROOT_BRIDGE_ID
	global DISTANCE_FROM_ROOT
	global BRIDGE_ID
	global BRIDGE_PORT_MAPPING_LOCAL
	global OUTGOING_MESSAGE_NUMBER

	print 'Readying BPDU'
	# printBridgeTable()

	# Outgoing socket
	s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	print 'Outgoing Sockets Created' ## Debugging

	# Define what will be sent in the BPDU. Store the value in message.
	Y =	ROOT_BRIDGE_ID	 			# Y is the bridge ID of the node that the sending bridge thinks is the root,
	if BRIDGE_ID == ROOT_BRIDGE_ID:
		d = 0
	else:
		d = DISTANCE_FROM_ROOT	 	 	# d is the cost to reach Y
	X =	BRIDGE_ID	 	 			# X is the bridge ID of the bridge sending the message.
	bpdu_message = str(Y) + ' ' + str(d) + ' ' + str(X)

	if (not bpdu_message):
		print 'WARNING SENDING EMPTY BPDU'

	for rowEntry in Bridge_Table:
		# Broadcast BPDU to DP designated ports
		if rowEntry[2] == "DP":
			if rowEntry == Bridge_Table[0]:
				# print 'bpdu data'
				# print 'msg ' + bpdu_message
				# print 'Sending Port ' + str(BRIDGE_PORT_MAPPING_LOCAL[0][1])
				# print 'IP: ' + BRIDGE_PORT_MAPPING_LOCAL[0][0]
				# print 'Root Port ' + str(BRIDGE_PORT_MAPPING_LOCAL[0][1])

				# print bpdu_message + ' ' + str(BRIDGE_PORT_MAPPING_LOCAL[0][1])

				print '\nOutgoing message ' + str(OUTGOING_MESSAGE_NUMBER)
				OUTGOING_MESSAGE_NUMBER = OUTGOING_MESSAGE_NUMBER + 1
				print bpdu_message + ' ' + str(BRIDGE_PORT_MAPPING_LOCAL[0][1])
				s1.sendto((bpdu_message + ' ' + str(BRIDGE_PORT_MAPPING_LOCAL[0][1])), (BRIDGE_PORT_MAPPING_LOCAL[0][0], int(BRIDGE_PORT_MAPPING_LOCAL[0][1])))  #(msg, ip, port)
				print 'message sent\n'

			elif rowEntry == Bridge_Table[1]:
				print '\nOutgoing message ' + str(OUTGOING_MESSAGE_NUMBER)
				OUTGOING_MESSAGE_NUMBER = OUTGOING_MESSAGE_NUMBER + 1
				print bpdu_message + ' ' + str(BRIDGE_PORT_MAPPING_LOCAL[1][1])
				s2.sendto((bpdu_message + ' ' + str(BRIDGE_PORT_MAPPING_LOCAL[1][1])), (BRIDGE_PORT_MAPPING_LOCAL[1][0], int(BRIDGE_PORT_MAPPING_LOCAL[1][1])))  #(msg, ip, port)
				print 'message sent\n'

			elif rowEntry == Bridge_Table[2]:

				print '\nOutgoing message ' + str(OUTGOING_MESSAGE_NUMBER)
				OUTGOING_MESSAGE_NUMBER = OUTGOING_MESSAGE_NUMBER + 1
				print bpdu_message + ' ' + str(BRIDGE_PORT_MAPPING_LOCAL[2][1])
				s3.sendto((bpdu_message + ' ' + str(BRIDGE_PORT_MAPPING_LOCAL[2][1])), (BRIDGE_PORT_MAPPING_LOCAL[2][0], int(BRIDGE_PORT_MAPPING_LOCAL[2][1])))  #(msg, ip, port)
				print 'message sent\n'

			else:
				print 'No DP\'s'
			# if rowEntry == Bridge_Table[0]:
			# 	print 'bpdu data'
			# 	print 'msg ' + bpdu_message
			# 	print 'Sending Port ' + str(BRIDGE_PORT_MAPPING_LOCAL[0][1])
			# 	print 'IP: ' + BRIDGE_PORT_MAPPING_LOCAL[0][0]
			# 	print 'Root Port ' + str(BRIDGE_PORT_MAPPING_LOCAL[0][1])
            #
			# 	# Reminder BRIDGE_ONE_PORT_MAPPING   = {(BRIDGE_TWO_IP, PORT_THREE), (BRIDGE_THREE_IP, PORT_ONE), (BRIDGE_FOUR_IP ,PORT_TWO)}
			# 	s.sendto(bpdu_message + ' ' + str(BRIDGE_PORT_MAPPING_LOCAL[0][1]) , ( BRIDGE_PORT_MAPPING_LOCAL[0][0], int(BRIDGE_PORT_MAPPING_LOCAL[0][1]) ) )  #(msg, ip, port)
			# elif rowEntry == Bridge_Table[1]:
			# 	s.sendto(bpdu_message + ' ' + str(BRIDGE_PORT_MAPPING_LOCAL[1][1]), (BRIDGE_PORT_MAPPING_LOCAL[1][0], int(BRIDGE_PORT_MAPPING_LOCAL[1][1])))
			# elif rowEntry == Bridge_Table[2]:
			# 	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			# 	s.sendto(bpdu_message + ' ' + str(BRIDGE_PORT_MAPPING_LOCAL[2][1]), (BRIDGE_PORT_MAPPING_LOCAL[2][0], int(BRIDGE_PORT_MAPPING_LOCAL[2][1])))
			# else:
			# 	'No DP\'s'

	# s1.close() # close socket
	# s2.close()
	# s3.close()

	if (ROOT_BRIDGE_ID == BRIDGE_ID):
		threading.Timer(5.0,sendBPDU,('garbage',)).start()
		sys.exit()
	else:
		print 'End of sendBPDU: I am no longer root. My MAC: ' + str(BRIDGE_ID) + ' Root MAC: ' + str(ROOT_BRIDGE_ID)
		print 'State of the Table'
		printBridgeTable()
		return True

	return True

def compareMAC(other_bridge_id, local_bridge):
	print 'in compareMAC'                            # Debugging
	print 'other_bridge_id: ' + other_bridge_id      # Debugging
	print 'local_bridge:    ' + local_bridge         # Debugging

	obi = other_bridge_id.split(':',6)
	print 'obi values:   ' + str(obi)                # Debugging
	lb = local_bridge.split(':',6)
	print 'lb values:    ' + str(lb)	             # Debugging

	if int(obi[0], 16) < int(lb[0],16):
		print obi[0] + ' < ' + lb[0]
		return True
	elif int(obi[0], 16) == int(lb[0],16):
		if int(obi[1],16) < int(lb[1], 16):
			print obi[1] + ' < ' + lb[1]
			return True
		elif int(obi[1],16) == int(lb[1], 16):
			if int(obi[2], 16) < int(lb[2], 16):
				print obi[2] + ' < ' + lb[2]
				return True
			elif int(obi[2], 16) == int(lb[2], 16):
				if int(obi[3], 16) < int(lb[3], 16):
					print obi[3] + ' < ' + lb[3]
					return True
				elif int(obi[3], 16) == int(lb[3], 16):
					if int(obi[4], 16) < int(lb[4], 16):
						print obi[4] + ' < ' + lb[4]
						return True
					elif int(obi[4], 16) < int(lb[4], 16):
						if int(obi[5], 16) < int(lb[5], 16):
							print obi[5] + ' < ' + lb[5]
							return True
						elif int(obi[5], 16) < int(lb[5], 16):
							print 'SAME MACS - something went wrong.'
	else:
		return False

def forwardBPDU():
	print 'FORWARDING BPDU to'
	print '------------------------'
	printBridgeTable()
	print '========================'
	sendBPDU('garbage')
	print 'BPDU FORWARDED '
	return True

#Function for handling connections. This will be used to create threads
def checkBPDU(data):
	global Bridge_Table
	global ROOT_BRIDGE_ID
	global DISTANCE_FROM_ROOT
	global BRIDGE_ID

	# Use split to parse data. First parameter is delimeter. Second parameter is number of cuts.

	if data:
		print '\nReceived BPDU, data received: ' + data
		user_input = data.split(" ")
		print 'data split ' + str(user_input)

		Y = str(user_input[0])       #root
		d = int(user_input[1])
		X = str(user_input[2])
		port = int(user_input[3])
		print 'port ' + str(port)


		# if Root ID = BRIDGE ID throw away
		if (Y == BRIDGE_ID):
			# for rowEntry in Bridge_Table:
			# 	if rowEntry[1] == port:
			# 		rowEntry[2] = "BP"
			# 		print 'Root Bridge assigned'
			# 		# printBridgeTable()
			return

		# PHASE 1 Elect a Root Bridge.
		# When comparing bridges, the priority is compared first ansd only if tghey are
		# equal is the MAC address compared.
		# The switch with the lowest priorty or lowest MAC addess in case ofequal priority
		# will be the root.
		if Y != ROOT_BRIDGE_ID:
			print 'DIFFERENT ROOT BRIDGE'    # Debugging
			print 'comparing Y with root bridge'	 # Debugging
			print 'if compareMAC(Y, ROOT_BRIDGE_ID):  ## ' + Y + ' ' + ROOT_BRIDGE_ID
			if compareMAC(Y, ROOT_BRIDGE_ID): # returns true if left parameter is less than right
				ROOT_BRIDGE_ID = Y
				DISTANCE_FROM_ROOT = d + 1

				# Change old RP to BP
				for rowEntry in Bridge_Table:
					if rowEntry[2] == 'RP':
						rowEntry[2] = 'BP'

				# Update port to be root port
				for rowEntry in Bridge_Table:
					if rowEntry[1] == port:
						rowEntry[2] = "RP"
						print 'Root Bridge assigned to table'
						# printBridgeTable()
				print str(BRIDGE_ID) + ' no longer root. ' + str(ROOT_BRIDGE_ID) + ' is the NEW ROOT'
			# else:
				# # Change Bridge Table
				# for rowEntry in Bridge_Table:
				# 	if Bridge_Table[1] == port:
				# 		Bridge_Table[2] = "BP"

			printBridgeTable() # Debugging

		# Phase 3 Each non-root switch selects its root port
		elif (Y == ROOT_BRIDGE_ID and ROOT_BRIDGE_ID != BRIDGE_ID):
			print '\nSAME ROOT BRIDGE'    # Debugging
			print 'comparing distances ' + str(d) + ' ' + str(DISTANCE_FROM_ROOT)	 # Debugging
			if(d < DISTANCE_FROM_ROOT):
				print 'Other Bridge is Closer Setting Port to RP'
				DISTANCE_FROM_ROOT = d + 1
				# Change old RP to BP state
				for rowEntry in Bridge_Table:
					if rowEntry[2] == 'RP':
						rowEntry[2] = 'BP'
				# Update new RP
				for rowEntry in Bridge_Table:
					if rowEntry[1] == port:
						rowEntry[2] = "RP"
			else:
				print 'Other Bridge is Further. Setting port to BP'
				# Change port to BP in Bridge Table
				for rowEntry in Bridge_Table:
					if rowEntry[1] == port:
						rowEntry[2] = "BP"


		if(BRIDGE_ID != ROOT_BRIDGE_ID):
			forwardBPDU()
			print 'End of checkBPDU: I am not root. My MAC: ' + str(BRIDGE_ID) + ' Root MAC: ' + str(ROOT_BRIDGE_ID)
			print 'State of the Table'
			printBridgeTable()
			return True
		# 	return
		# else:
		# 	print ' Im the Root my thread will respawn shortly.'
	return True



def accept_connections_on_port_one(args):
	# Declare Ports and set up socket type
	Port1_to_Bridge = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	print 'Port 1 to Bridge Socket created.'

	Port1_to_Bridge.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	try:
		print 'Port1_to_Bridge.bind((LOCAL_HOST, PORT_ONE)) # ' + LOCAL_HOST + ', ' + str(PORT_ONE) # debugging
		Port1_to_Bridge.bind((LOCAL_HOST, PORT_ONE))
	except socket.error , msg:
		print LOCAL_BRIDGE_IP + 'Bridges Bind failed. Error Code: ' + str(msg[0]) + ' Message ' + msg[1]
		sys.exit()

	print 'Port 1 waiting for connection'
	while 1:
		print 'Port 1 listening'
  		data, addr = Port1_to_Bridge.recvfrom(512)
		if data:
			#start_new_thread(checkBPDU, (data,) )
			checkBPDU(data)
		# print 'i run forever dude.' # debugging
	print 'THREAD EXITED'

def accept_connections_on_port_two(args):
	Port2_to_Bridge = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	print 'Port 2 to Bridge Socket created.'

	Port2_to_Bridge.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	try:
		print 'Port1_to_Bridge.bind((LOCAL_HOST, PORT_TWO)) # ' + LOCAL_HOST + ', ' + str(PORT_TWO) # debugging
		Port2_to_Bridge.bind((LOCAL_HOST, PORT_TWO))
	except socket.error , msg:
		print LOCAL_BRIDGE_IP + 'Bridges Bind failed. Error Code: ' + str(msg[0]) + ' Message ' + msg[1]
		sys.exit()

	print 'Port 2 waiting for connection'
	while 1:
		print 'Port 2 listening'
		data, addr = Port2_to_Bridge.recvfrom(512)
  		if data:
			#start_new_thread(checkBPDU, (data,) )
			checkBPDU(data)
		# print 'i run forever dude.' # debugging
	print 'THREAD EXITED'

def accept_connections_on_port_three(args):
	Port3_to_Bridge = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	print 'Port 3 to Bridge Socket created.'

	Port3_to_Bridge.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	try:
		print 'Port1_to_Bridge.bind((LOCAL_HOST, PORT_THREE)) # ' + LOCAL_HOST + ', ' + str(PORT_THREE) # debugging
		Port3_to_Bridge.bind((LOCAL_HOST, PORT_THREE))
	except socket.error , msg:
		print LOCAL_BRIDGE_IP + 'Bridges Bind failed. Error Code: ' + str(msg[0]) + ' Message ' + msg[1]
		sys.exit()

	print 'Port 3 waiting for connection'
	while 1:
		print 'Port 3 listening'
  		data, addr = Port3_to_Bridge.recvfrom(512)
		if data:
			#start_new_thread(checkBPDU, (data,) )
			checkBPDU(data)
		# print 'i run forever dude.' # debugging
	print 'THREAD EXITED'


# setup_bridge identifies the bridge's ip and begins to setting up the
# required connections based on the required port map.

def clientThread(conn):
	print 'Made it to client thread\n'
	while True:
		print 'Port listening...'
  		data, addr = conn.recvfrom(1024)
		print 'data received: ' + str(data)
		if data:
			#start_new_thread(checkBPDU, (data,) )
			print 'Calling checkBPDU(data)'
			checkBPDU(data)
		print 'i run forever dude.' # debugging
	print 'THREAD EXITED'


def setup_bridge(Bridge_IP):
	global LOCAL_PORT       # Arbitrary non-privileged port
	global LOCAL_HOST
	global LOCAL_BRIDGE_IP
	global LOCAL_BRIDGE_MAC

	print 'Local ' + LOCAL_BRIDGE_MAC # Debugging

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
	print 'Initial Table'
	print Bridge_Table
	# args = (10,)
	# start_new_thread(accept_connections_on_port_one, args )
	# time.sleep(1)
	# start_new_thread(accept_connections_on_port_two, args)
	# time.sleep(1)
	# start_new_thread(accept_connections_on_port_three, args)


	# test



	# Declare Ports and set up socket type
	Port1_to_Bridge = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	print 'Port 1 to Bridge Socket created.'
	Port1_to_Bridge.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	try:
		print 'Port1_to_Bridge.bind((LOCAL_HOST, PORT_ONE)) # ' + LOCAL_HOST + ', ' + str(PORT_ONE) # debugging
		Port1_to_Bridge.bind((LOCAL_HOST, PORT_ONE))
	except socket.error , msg:
		print LOCAL_BRIDGE_IP + 'Bridges Bind failed. Error Code: ' + str(msg[0]) + ' Message ' + msg[1]
		sys.exit()
	print 'Port 1 waiting for connection'

	start_new_thread(clientThread,(Port1_to_Bridge,))


	Port2_to_Bridge = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	print 'Port 2 to Bridge Socket created.'
	Port2_to_Bridge.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	try:
		print 'Port1_to_Bridge.bind((LOCAL_HOST, PORT_TWO)) # ' + LOCAL_HOST + ', ' + str(PORT_TWO) # debugging
		Port2_to_Bridge.bind((LOCAL_HOST, PORT_TWO))
	except socket.error , msg:
		print LOCAL_BRIDGE_IP + 'Bridges Bind failed. Error Code: ' + str(msg[0]) + ' Message ' + msg[1]
		sys.exit()
	print 'Port 2 waiting for connection'
	start_new_thread(clientThread, (Port2_to_Bridge,))

	Port3_to_Bridge = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	print 'Port 3 to Bridge Socket created.'
	Port3_to_Bridge.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	try:
		print 'Port1_to_Bridge.bind((LOCAL_HOST, PORT_THREE)) # ' + LOCAL_HOST + ', ' + str(PORT_THREE) # debugging
		Port3_to_Bridge.bind((LOCAL_HOST, PORT_THREE))
	except socket.error , msg:
		print LOCAL_BRIDGE_IP + 'Bridges Bind failed. Error Code: ' + str(msg[0]) + ' Message ' + msg[1]
		sys.exit()
	print 'Port 3 waiting for connection'


	start_new_thread(clientThread,(Port3_to_Bridge,))
	# To avoid port reuse problem, the function below is used
	# Port1_to_Bridge.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	# Port2_to_Bridge.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	# Port3_to_Bridge.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	# print 'Starting algorithm in 10 seconds'
	# time.sleep(5)
	# print 'Starting algorithm in 5 seconds'
	# time.sleep(2)
	# print 'Starting algorithm in 3 seconds'
	# time.sleep(1)
	# print 'Starting algorithm in 2 seconds'
	# time.sleep(1)
	# print 'Starting algorithm in 1 seconds'
	# time.sleep(1)
	# print 'Start!'
	args = 'garbage'

	start_new_thread(sendBPDU,(args,))

	while 1:
		pass
	print 'End of Setup Bridge reached'

	return True
	#now keep talking with the client
	# threading.Timer(5.0,sendBPDU).start()


if __name__ == '__main__':
	if len(sys.argv) > 1:
		print("python Bridge.py")
		quit(1)
	result = setup_bridge(LOCAL_BRIDGE_IP)

print 'We in outer space now'
