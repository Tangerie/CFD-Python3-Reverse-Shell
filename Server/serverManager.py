import socket, os, sys, time, base64

connectedPorts = []
connectedPortInfo = []
availablePorts = [1338, 1339, 1340]

deletePortFile = "delPort.txt"
currentPortsFile = "currentPorts.txt"

serverIP = "localhost"

loopTime = 5

def createSocket():
	try:
		global host
		global port
		global s

		socket.setdefaulttimeout(loopTime)
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		host = ''
		try:
			port = sys.argv[1]
		except:
			port = input('Type Port For Listening: ')

		while not port:
			port = input('Type Port For Listening: ')

		port = int(port)
	except socket.error as msg:
		print('Socket Error:', msg)

def bindSocket():
	try:
		print('Binding Socket To Port:', port)

		s.bind((host,port))

		s.listen(1)

	except socket.error as msg:
		print('Socket Binding Error:', msg)

		bindSocket()

def acceptSocket():
	global conn
	global addr

	#Check if connections must be removed
	if os.path.isfile(deletePortFile):
		f = open(deletePortFile)
		text = f.read()
		index = connectedPorts.index(int(text))
		del connectedPorts[index]
		del connectedPortInfo[index]
		print("Deleting Port: " + text)
		f.close()
		os.remove(deletePortFile)
		updatePortFile()

	#Check to add more connections
	if len(availablePorts) < 1:
		return

	try:
		conn, addr = s.accept()
		print('Session Opend at %s:%s \n'%(addr[0], addr[1]))

		sentPort = availablePorts[0]
		del availablePorts[0]

		data = conn.recv(1024).decode().split(',')
		print(data)
		hostname = str(data[0])
		operatingSystem = str(data[1])

		connectedPortInfo.append([hostname, operatingSystem])

		connectedPorts.append(sentPort)
		updatePortFile()
		conn.send((str(sentPort) + "," + serverIP).encode('utf8'))
		conn.close()
		print(hostname + "(" + operatingSystem + ") - " + str(sentPort) + ' - ' + serverIP)
	except socket.error as msg:
		pass


def updatePortFile():
	f = open(currentPortsFile, "w+")
	for i in range(len(connectedPorts)):
		f.write(connectedPortInfo[i][0] + "(" + connectedPortInfo[i][1] + ") - " + str(connectedPorts[i]) + ' - ' + serverIP + "\n")
	f.close()

def main():
	if os.path.isfile(deletePortFile):
		os.remove(deletePortFile)

	if os.path.isfile(currentPortsFile):
		os.remove(currentPortsFile)

	createSocket()
	bindSocket()
	while True:
		acceptSocket()

main()