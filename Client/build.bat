pyinstaller --onefile --windowed clientWindows.py
move dist\clientWindows.exe ..\Builds\
rmdir /Q /s build
rmdir /Q /s dist
del /Q clientWindows.spec
start ..\Builds\
