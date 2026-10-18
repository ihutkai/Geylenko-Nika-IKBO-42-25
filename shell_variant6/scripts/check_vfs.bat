@echo off
setlocal
cd /d "%~dp0.."
echo Close each emulator window to continue to the next example.
python src\main.py --vfs examples\minimal.json --startup examples\stage3.txt
python src\main.py --vfs examples\vfs.json --startup examples\stage3.txt
python src\main.py --vfs examples\deep.json --startup examples\stage3.txt
pause
