# Python3 Reverse Shell

## Setup

###### Server Side
1. Install needed python components
	```
	pip install -r requirements.txt
	```

2. Start server with:
	```
	python server.py
	```
	And enter the port number you wish to use

3. Run keylogServer.py
	```
	python keylogServer.py [desired port]
	```
	Note this port must be different from the one entered beforehand

4. Edit clientWindows.py and change your host and port to those of your server, make sure to enter the first port you entered into server.py

###### Client Side
1. Run clientWindows.py with
	```
	python clientWindows.py
	```
	Or compile clientWindows.py into and exe with pythoninstaller and run it as normal

## Commands
*Note: Commands ignore captilisation, but arguments maintain capitilisation*

**quit**

	Exits the shell on both server and client sides


**shell**

	Runs commands in that OSes shell


**shellThread**

	Same as shell but runs commands on a separate thread incase they dont exit(note, you cannot return values from this command)


**cwd**

	Returns the current directory


**ls**

	Lists files and folders in current directory


**cd [*directory*]**

	Changes to given directory


**cat [*filename*]**

	Outputs contents of the given file, note: only works with human readable files, it will crash otherwise


**keylog [*port*]**

	Runs the keylogger on given port, make sure to run keylogServer.py and use the same port for both commands


**killkeylog**

	Kills the keylogger if currently running


## TODO
 - [X] Make Keylogger
 - [X] Add Keylogger to program
 - [ ] Add extra commands