@echo off
setlocal
cd /d "%~dp0.."
echo Close each emulator window to continue to the next example.
python src\main.py --vfs examples\custom.json
python src\main.py --startup examples\missing.txt
python src\main.py --config examples\missing.toml
python src\main.py --config examples\bad-config.toml
python src\main.py --config config.toml --vfs examples\override.json --startup examples\startup.txt
python src\main.py --startup examples\exit.txt
pause
