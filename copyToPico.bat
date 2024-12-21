@echo off
set DESTINATION=F:\
copy display.py %DESTINATION%
copy ledNormal.py %DESTINATION%
copy switchAndLed.py %DESTINATION%
copy hardware.py %DESTINATION%
copy tools.py %DESTINATION%
copy game.py %DESTINATION%
copy power.py %DESTINATION%
copy main.py %DESTINATION%

echo Files copied successfully to %DESTINATION%.
