import socket, os, sys
def createSocket():
	try:
		global host
		global port
		global s

		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		host = ''
		port = input('Type Port For Listening: ')

		if port == '':
			createSocket()
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

	try:
		conn, addr = s.accept()
		print('Session Opend at %s:%s \n'%(addr[0], addr[1]))
		hostname = conn.recv(1024).decode()
		print(hostname)
		menu()
	except socket.error as msg:
		print('Socket Accepting Error:', msg)

def menu():
	while True:
		cmd = input(str(addr[0]) + '@' + str(hostname) + '> ')
		while cmd == "":
			cmd = input(str(addr[0]) + '@' + str(hostname) + '> ')
		if cmd == 'quit':
			conn.close()
			s.close()
			sys.exit()

		command = conn.send(cmd.encode('utf8'))
		result = conn.recv(16834)

		if result != hostname:
			print(result.decode())

def main():
	createSocket()
	bindSocket()
	acceptSocket()

main()