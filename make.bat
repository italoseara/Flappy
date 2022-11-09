@echo off

set ARG=%1
set PYCMD=

where /q py && set PYCMD=py
where /q python && set PYCMD=python
where /q python3 && set PYCMD=python
where /q python3.7 && set PYCMD=python
where /q python3.8 && set PYCMD=python

if "%PYCMD%" == "" (
   echo Could not find python binary in PATH.
   exit /b
)

rem TODO: iterate through arguments instead of only reading arg #1
if "%1" == "pip" (
   %PYCMD% -m pip install pygame
   %PYCMD% -m pip install pyinstaller
) else if "%1" == "run" (
   cd src
   %PYCMD% main.py
   cd ..
) else if "%1" == "install" (
  pyinstaller --noconfirm --onedir --windowed --icon "src/resources/app_icon.ico" --name "Flappy Bird" --add-data "src/audio;audio/" --add-data "src/core;core/" --add-data "src/game;game/" --add-data "src/resources;resources/" "src/main.py"
) else (
   echo Unknown subcommand: "%1"
   goto usage
)

goto end

:usage
echo Usage: %0 { pip ^| run }
exit /b

:end
@echo on
