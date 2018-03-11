import socket
UDP_IP = "10.0.0.2"  # The address of the receiver
UDP_PORT = 8002      # The port the receiver will be listening to.
MESSAGE = "Hello, Python from UDP World Port " + str(UDP_PORT) + "!"

my_skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_skt.connect((UDP_IP, UDP_PORT))
my_skt.send(MESSAGE)

print 'Message sent'
