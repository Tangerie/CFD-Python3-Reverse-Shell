# Python3 Reverse Shell

## Setup

###### Server Side
1. Install needed python components

		pip install -r requirements.txt

2. Start server with:

		python Server/server.py

	And enter the port number you wish to use

	OR

		python Server/server.py [desired port]

3. Run keylogServer.py
		python Server/keylogServer.py

	And enter the desired port

	OR

		python Server/keylogServer.py [desired port]

	*Note this port must be different from the one entered beforehand*

4. Edit clientWindows.py and change your host and port to those of your server, make sure to enter the first port you entered into server.py.
	
	OR

	Add in a url for port and host, the program will retrieve its port or ip from that url in raw text form

###### Client Side
1. Run clientWindows.py with

		python Client/clientWindows.py

	Or compile clientWindows.py into and exe with pythoninstaller and run it as a normal executable

## Commands
*Note: Commands ignore captilisation, but arguments maintain capitilisation*

**quit**

	Cleanly shuts the connection on both server and client sides and quits the client service - NOTE: Only recommended for removal as all control is lost until client run again

**reset**
	
	Cuts the connection, but does not quit the client - Recommened if you just need to restart the connection


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

*NOTE - Keylogger currently only works on windows, it is untested on other platforms and will definitely crash*

**killkeylog**

	Kills the keylogger if currently running


## TODO
 - [X] Make Keylogger
 - [X] Add Keylogger to program
 - [ ] Add extra commands