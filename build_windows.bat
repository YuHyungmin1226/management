@echo off
echo 학생 관리 시스템 - Windows 빌드 스크립트
echo.

REM Python 설치 확인
python --version >nul 2>&1
if errorlevel 1 (
    echo Python이 설치되지 않았습니다.
    echo https://www.python.org/downloads/ 에서 Python을 다운로드하여 설치하세요.
    pause
    exit /b 1
)

REM PyInstaller 설치 확인
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller를 설치합니다...
    pip install pyinstaller
)

REM 의존성 설치
echo 의존성을 설치합니다...
pip install -r requirements.txt

REM 빌드 실행
echo Windows용 실행 파일을 빌드합니다...
pyinstaller --onefile --add-data "templates;templates" --hidden-import=mmap --hidden-import=multiprocessing --hidden-import=_csv --name "student_management" management_app.py

REM 빌드 결과 확인
if exist "dist\student_management.exe" (
    echo.
    echo 빌드 성공!
    echo dist\student_management.exe 파일을 student_management_portable 폴더로 복사하세요.
    echo.
    copy "dist\student_management.exe" "student_management_portable\student_management.exe"
    echo 파일이 복사되었습니다.
) else (
    echo.
    echo 빌드 실패!
    echo 오류 메시지를 확인하세요.
)

pause
