@echo off
setlocal
cd /d "%~dp0.."
echo Close each emulator window to continue to the next example.
python src\main.py --vfs examples\minimal.json
python src\main.py --vfs examples\vfs.json
python src\main.py --vfs examples\deep.json
python src\main.py --vfs examples\missing.json
python src\main.py --vfs examples\bad-json.json
python src\main.py --vfs examples\bad-vfs.json
python src\main.py --vfs examples\bad-base64.json
pause
