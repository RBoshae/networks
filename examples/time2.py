import threading

def set_timer():
	threading.Timer(5.0,set_timer).start()
	print 'Print every 5s'

set_timer()
