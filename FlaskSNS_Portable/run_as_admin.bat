@echo off
echo Flask SNS 포터블 앱을 관리자 권한으로 실행합니다...
powershell -Command "Start-Process FlaskSNS.exe -Verb RunAs"
pause
