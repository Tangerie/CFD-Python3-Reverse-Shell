pyinstaller --onefile server.py
move dist\server.exe ..\Builds\
rmdir /Q /s build
rmdir /Q /s dist
del /Q server.spec
start ..\Builds\
