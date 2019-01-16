pyinstaller --onefile keylogServer.py
move dist\keylogServer.exe ..\Builds\
rmdir /Q /s build
rmdir /Q /s dist
del /Q keylogServer.spec
start ..\Builds\
