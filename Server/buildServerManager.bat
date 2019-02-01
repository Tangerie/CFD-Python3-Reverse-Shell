pyinstaller --onefile serverManager.py
move dist\serverManager.exe ..\Builds\
rmdir /Q /s build
rmdir /Q /s dist
del /Q serverManager.spec
start ..\Builds\
