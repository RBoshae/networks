import socket
import sys

UDP_IP = "10.0.0.2"  # This is the address where the receiver is running
UDP_PORT = 8002      # This needs to match the port the sender is sending to.

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP

#To avoid port reuse problem, the function below is used
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    sock.bind((UDP_IP, UDP_PORT))
except socket.error , msg:
    print ' Bind failed. Error Code: ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

while True:
    data, addr = sock.recvfrom(512) # buffer size is 1024 bytes
    print "received message:"
