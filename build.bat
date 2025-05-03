@echo off

echo Cleaning up old build artifacts...
rmdir /S /Q build
rmdir /S /Q dist

echo Building the project...
pyinstaller pyinstaller\LearnAnalogClocks.spec

pause
