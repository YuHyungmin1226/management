#!/bin/bash

echo "학생 관리 시스템 - macOS 개선된 빌드 스크립트"
echo "=============================================="

# Python 설치 확인
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3이 설치되지 않았습니다."
    echo "https://www.python.org/downloads/ 에서 Python을 다운로드하여 설치하세요."
    exit 1
fi

echo "✅ Python3 확인됨: $(python3 --version)"

# PyInstaller 설치 확인 및 업데이트
if ! pip3 show pyinstaller &> /dev/null; then
    echo "📦 PyInstaller를 설치합니다..."
    pip3 install pyinstaller
else
    echo "🔄 PyInstaller를 최신 버전으로 업데이트합니다..."
    pip3 install --upgrade pyinstaller
fi

# 의존성 설치
echo "📦 의존성을 설치합니다..."
pip3 install -r requirements.txt

# 기존 빌드 파일 정리
echo "🧹 기존 빌드 파일을 정리합니다..."
rm -rf build dist *.spec

# 빌드 실행
echo "🔨 macOS용 실행 파일을 빌드합니다..."
echo "   - Universal Binary (Intel + Apple Silicon) 지원"
echo "   - 템플릿 파일 포함"
echo "   - 숨겨진 의존성 포함"

# Universal Binary 빌드 시도
echo "🔄 Universal Binary 빌드를 시도합니다..."
if pyinstaller \
    --onefile \
    --add-data "templates:templates" \
    --hidden-import=mmap \
    --hidden-import=multiprocessing \
    --hidden-import=_csv \
    --hidden-import=sqlite3 \
    --hidden-import=flask \
    --hidden-import=flask_sqlalchemy \
    --hidden-import=flask_wtf \
    --name "학생관리시스템_mac" \
    --target-architecture universal2 \
    --clean \
    management_app.py 2>/dev/null; then
    echo "✅ Universal Binary 빌드 성공!"
else
    echo "⚠️  Universal Binary 빌드 실패, 현재 아키텍처로 빌드합니다..."
    pyinstaller \
        --onefile \
        --add-data "templates:templates" \
        --hidden-import=mmap \
        --hidden-import=multiprocessing \
        --hidden-import=_csv \
        --hidden-import=sqlite3 \
        --hidden-import=flask \
        --hidden-import=flask_sqlalchemy \
        --hidden-import=flask_wtf \
        --name "학생관리시스템_mac" \
        --clean \
        management_app.py
fi

# 빌드 결과 확인
if [ -f "dist/학생관리시스템_mac" ]; then
    echo
    echo "✅ 빌드 성공!"
    echo "📁 파일 정보:"
    ls -lh "dist/학생관리시스템_mac"
    
    echo
    echo "🏗️  아키텍처 정보:"
    lipo -info "dist/학생관리시스템_mac"
    
    echo
    echo "📋 파일을 student_management_portable 폴더로 복사합니다..."
    cp "dist/학생관리시스템_mac" "student_management_portable/student_management_mac"
    chmod +x "student_management_portable/student_management_mac"
    
    echo "✅ 파일이 복사되었습니다."
    echo "✅ 실행 권한이 설정되었습니다."
    
    echo
    echo "🧪 테스트 실행:"
    echo "cd student_management_portable && ./student_management_mac"
    
else
    echo
    echo "❌ 빌드 실패!"
    echo "오류 메시지를 확인하세요."
    exit 1
fi

echo
echo "🎉 빌드 완료!"
