:Start
DEL /F /Q screen_1.m3u
FOR /F "tokens=1 delims=" %%A IN ('DIR /B %CD%\screen_1') DO ECHO %CD%\screen_1\%%A >> screen_1.m3u

DEL /F /Q screen_2.m3u
FOR /F "tokens=1 delims=" %%A IN ('DIR /B %CD%\screen_2') DO ECHO %CD%\screen_2\%%A >> screen_2.m3u


DEL /F /Q screen_3.m3u
FOR /F "tokens=1 delims=" %%A IN ('DIR /B %CD%\screen_3') DO ECHO %CD%\screen_3\%%A >> screen_3.m3u


DEL /F /Q screen_4.m3u
FOR /F "tokens=1 delims=" %%A IN ('DIR /B %CD%\screen_4') DO ECHO %CD%\screen_4\%%A >> screen_4.m3u

DEL /F /Q screen_5.m3u
FOR /F "tokens=1 delims=" %%A IN ('DIR /B %CD%\screen_5') DO ECHO %CD%\screen_5\%%A >> screen_5.m3u

DEL /F /Q screen_6.m3u
FOR /F "tokens=1 delims=" %%A IN ('DIR /B %CD%\screen_6') DO ECHO %CD%\screen_6\%%A >> screen_6.m3u

START vlc.exe --http-port=8080 screen_1.m3u
START vlc.exe --http-port=8081 screen_2.m3u
START vlc.exe --http-port=8082 screen_3.m3u
START vlc.exe --http-port=8083 screen_4.m3u
START vlc.exe --http-port=8084 screen_5.m3u
START vlc.exe --http-port=8085 screen_6.m3u


@echo off
python interface_six_screens.py %*
pause