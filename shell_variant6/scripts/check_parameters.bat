@echo off
setlocal
cd /d "%~dp0.."
echo Close each emulator window to continue to the next example.
python src\main.py
python src\main.py --vfs examples\minimal.json
python src\main.py --startup examples\startup.txt
python src\main.py --config config.toml
python src\main.py --config config.toml --vfs examples\deep.json --startup examples\exit.txt
pause
