import OSC
import time
from gtts import gTTS
import os
import socket
import threading
from OSC import OSCClient, OSCMessage
import collections
import time

client = OSCClient()
new_client = OSCClient()
new_client.connect(("127.0.0.1",12005))
#client.connect( ("127.0.0.1", 12000) )



array = []
current_output = 1.0
count = 0
not_count = 0

voice_addr = '127.0.0.1',12002
music_addr = '127.0.0.1',7110
#sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
#sock.bind((UDP_IP,UDP_PORT))
s = OSC.OSCServer(voice_addr)
#s.addDefaultHandlers()
s.timeout = 0
run = True

loop_element = 0
thread_flag = True


d = collections.deque([],maxlen = 10)

client_lock = threading.Lock()

def regression(value):



	msg = OSCMessage("wek/inputs")
	msg.append(value)

#	for i in range(20):
#		time.sleep(0.1)
	global client_lock
	with client_lock:

		new_client.send(msg)
	#new_client.send(msg)
	#new_client.send(msg)
	#new_client.send(msg)

	print "MSG - ",msg
	print "\n\nSent Regression Message"




def handle_timeout(self):
    self.timed_out = True

import types
s.handle_timeout = types.MethodType(handle_timeout, s)



def respond_voice(value):

	#print "Initialized respond"


	global current_output
	global d
	global not_count
	global thread_flag
	print "\nResponse Generating"
	#print d, current_output

	if d[0] != current_output:
		not_count = not_count + 1
		if not_count > 50:
			thread_flag = False

			if d[0] == 1.0 :
				print "Hello"
				speech('Hello')
				current_output = 1.0
			if d[0] == 2.0 :
				print "This"
				speech('This')
				current_output = 2.0
			if d[0] == 3.0 :
				print "is"
				speech('is')
				current_output = 3.0
			if d[0] == 4.0 :
				print "Awesome"
				speech('Awesome')
				current_output = 4.0
			if d[0] == 5.0 :
				print "Project"
				speech('Project')
				current_output = 5.0
			if d[0] == 6.0 :
				print "default"
				#speech('Awesome')
				current_output = 6.0
			if d[0] == 7.0 :
				print "send control"
				#speech('Awesome')
				t = threading.Thread(target = regression,args = (value,))
				t.start()
				#msg = OSCMessage("wek/inputs")
				#msg.append(value)
				#new_client.send(msg)

				current_output = 7.0

	thread_flag = True
	return





def response(path,tags, args, source):
	print args[0]
	global count
	global not_count
	global current_output
	global thread_flag

	global d
	d.append(args[0])
	#print "appending"
	#print d[0]
	if d[0] != current_output:
		print "thread_spawned"
		if thread_flag:
			print "inside"
			t = threading.Thread(target=respond_voice,args = (args[1],))
			t.start()
			print "done"






	#speech(str(chr(int(args[0]) + 97)))
'''
	global array
	global loop_element


	if args[0] == 0.0:
		print 'break'
		print array
		speech(array)
		array = []
	else:
		print args[0]
		array[loop_element] = chr(int(args[0]) + 97)
		loop_element = loop_element+1

'''


s.addMsgHandler("/wek/outputs",response)

def each_frame():
    # clear timed_out flag
    s.timed_out = False
    # handle all pending requests then return
    while not s.timed_out:
        s.handle_request()


def speech(input_text):

	tts = gTTS(text=input_text,lang = 'en')
	tts.save("good.mp3")
	os.system("mpg321 good.mp3")


def main():
    """This runs the protocol on port 8000"""
    inp = OSCMessage("/wekinator/control/setInputNames")
    inp.append('inp')
    new_client.send(inp)
    while run:
    	time.sleep(1)
    	each_frame()
    s.close()
'''
    while True:
    	data,addr = sock.recvfrom(1024)
    	print data
'''
	#time.sleep(2)


if __name__ == '__main__':
    main()


'''
for i in xrange(1,10):
	engine = pyttsx.init()
	engine.say('Hello Asshole')
	engine.runAndWait()
	engine.stop()
	print i
	time.sleep(10)
	'''
