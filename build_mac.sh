#!/bin/bash

echo "학생 관리 시스템 - macOS 빌드 스크립트"
echo

# Python 설치 확인
if ! command -v python3 &> /dev/null; then
    echo "Python3이 설치되지 않았습니다."
    echo "https://www.python.org/downloads/ 에서 Python을 다운로드하여 설치하세요."
    exit 1
fi

# PyInstaller 설치 확인
if ! pip3 show pyinstaller &> /dev/null; then
    echo "PyInstaller를 설치합니다..."
    pip3 install pyinstaller
fi

# 의존성 설치
echo "의존성을 설치합니다..."
pip3 install -r requirements.txt

# 빌드 실행
echo "macOS용 실행 파일을 빌드합니다..."
pyinstaller --onefile --add-data "templates:templates" --hidden-import=mmap --hidden-import=multiprocessing --hidden-import=_csv --name "학생관리시스템_mac" management_app.py

# 빌드 결과 확인
if [ -f "dist/학생관리시스템_mac" ]; then
    echo
    echo "빌드 성공!"
    echo "dist/학생관리시스템_mac 파일을 학생관리시스템_포터블 폴더로 복사합니다."
    echo
    cp "dist/학생관리시스템_mac" "학생관리시스템_포터블/학생관리시스템_mac"
    chmod +x "학생관리시스템_포터블/학생관리시스템_mac"
    echo "파일이 복사되었습니다."
else
    echo
    echo "빌드 실패!"
    echo "오류 메시지를 확인하세요."
fi
