:Start
DEL /F /Q screen_1.m3u
FOR /F "tokens=1 delims=" %%A IN ('DIR /B %CD%\screen_1') DO ECHO %CD%\screen_1\%%A >> screen_1.m3u

DEL /F /Q screen_2.m3u
FOR /F "tokens=1 delims=" %%A IN ('DIR /B %CD%\screen_2') DO ECHO %CD%\screen_2\%%A >> screen_2.m3u


START vlc.exe --http-port=8080 screen_1.m3u --no-directx-overlay --directx-device=\\.\DISPLAY1
START vlc.exe --http-port=8081 screen_2.m3u --no-directx-overlay --directx-device=\\.\DISPLAY2



@echo off
python interface_multiple_ip_concurrent.py %*
pause