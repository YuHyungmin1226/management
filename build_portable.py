#!/usr/bin/env python3
"""
Windows용 포터블 Flask SNS 앱 빌드 스크립트
USB에서 실행 가능한 단일 실행 파일 생성
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def check_pyinstaller():
    """PyInstaller 설치 확인 및 설치"""
    try:
        import PyInstaller
        print("✅ PyInstaller가 이미 설치되어 있습니다.")
    except ImportError:
        print("📦 PyInstaller를 설치합니다...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("✅ PyInstaller 설치 완료!")

def create_portable_build():
    """포터블 빌드 생성"""
    print("🚀 Windows용 포터블 빌드를 시작합니다...")
    
    # 빌드 디렉터리 생성
    build_dir = Path("portable_build")
    if build_dir.exists():
        shutil.rmtree(build_dir)
    build_dir.mkdir()
    
    # 현재 디렉터리 경로
    current_dir = os.getcwd()
    
    # PyInstaller 명령어 구성
    cmd = [
        "pyinstaller",
        "--onefile",                    # 단일 실행 파일
        "--console",                    # 콘솔 창 표시 (디버깅용)
        "--name=FlaskSNS",              # 실행 파일 이름
        "--distpath=portable_build",    # 출력 디렉터리
        "--workpath=build_temp",        # 임시 작업 디렉터리
        "--specpath=build_temp",        # spec 파일 위치
        f"--add-data={os.path.join(current_dir, 'templates')};templates",  # 템플릿 폴더 포함
        f"--add-data={os.path.join(current_dir, 'config')};config",        # 설정 폴더 포함
        f"--add-data={os.path.join(current_dir, 'utils')};utils",          # 유틸리티 폴더 포함
        "--hidden-import=flask",           # Flask 숨겨진 import
        "--hidden-import=flask_sqlalchemy",
        "--hidden-import=flask_login",
        "--hidden-import=werkzeug",
        "--hidden-import=jinja2",
        "--hidden-import=sqlalchemy",
        "--hidden-import=requests",
        "--hidden-import=beautifulsoup4",
        "--hidden-import=PIL",
        "--hidden-import=filetype",
        "--hidden-import=waitress",
        "run.py"                        # 메인 실행 파일
    ]
    
    print("🔨 PyInstaller로 빌드를 시작합니다...")
    print(f"명령어: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ 빌드 성공!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 빌드 실패: {e}")
        print(f"오류 출력: {e.stderr}")
        return False

def create_portable_package():
    """포터블 패키지 생성"""
    print("📦 포터블 패키지를 생성합니다...")
    
    # 포터블 디렉터리 생성
    portable_dir = Path("FlaskSNS_Portable")
    if portable_dir.exists():
        shutil.rmtree(portable_dir)
    portable_dir.mkdir()
    
    # 실행 파일 복사
    exe_path = Path("portable_build/FlaskSNS.exe")
    if exe_path.exists():
        shutil.copy2(exe_path, portable_dir / "FlaskSNS.exe")
        print("✅ 실행 파일 복사 완료")
    else:
        print("❌ 실행 파일을 찾을 수 없습니다!")
        return False
    
    # README 파일 생성
    readme_content = """# Flask SNS 포터블 버전

## 사용 방법

1. USB 드라이브에 이 폴더를 복사하세요
2. FlaskSNS.exe를 더블클릭하여 실행하세요
3. 웹 브라우저에서 http://localhost:5001 접속
4. 기본 계정: admin / admin123

## 주의사항

- Windows 10/11에서 실행됩니다
- 인터넷 연결이 필요합니다 (패키지 다운로드용)
- 첫 실행 시 데이터베이스가 자동으로 생성됩니다
- 종료하려면 Ctrl+C를 누르거나 창을 닫으세요

## 문제 해결

- 실행이 안 되는 경우: 관리자 권한으로 실행해보세요
- 포트 충돌 시: 다른 포트로 자동 변경됩니다
- 데이터베이스 오류: sns.db 파일을 삭제하고 다시 실행하세요

## 지원

문제가 있으면 GitHub 이슈를 생성해주세요.
"""
    
    with open(portable_dir / "README.txt", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print("✅ README 파일 생성 완료")
    
    # 배치 파일 생성 (관리자 권한 실행용)
    batch_content = """@echo off
echo Flask SNS 포터블 버전을 시작합니다...
echo 관리자 권한으로 실행 중...
FlaskSNS.exe
pause
"""
    
    with open(portable_dir / "run_as_admin.bat", "w", encoding="utf-8") as f:
        f.write(batch_content)
    
    print("✅ 관리자 권한 실행 배치 파일 생성 완료")
    
    return True

def cleanup():
    """임시 파일 정리"""
    print("🧹 임시 파일을 정리합니다...")
    
    temp_dirs = ["build_temp", "portable_build", "__pycache__"]
    for temp_dir in temp_dirs:
        if Path(temp_dir).exists():
            shutil.rmtree(temp_dir)
            print(f"✅ {temp_dir} 삭제 완료")
    
    # spec 파일 삭제
    spec_file = Path("FlaskSNS.spec")
    if spec_file.exists():
        spec_file.unlink()
        print("✅ spec 파일 삭제 완료")

def main():
    """메인 함수"""
    print("=" * 50)
    print("Windows용 Flask SNS 포터블 빌드 도구")
    print("=" * 50)
    
    # PyInstaller 확인
    check_pyinstaller()
    
    # 빌드 실행
    if create_portable_build():
        # 포터블 패키지 생성
        if create_portable_package():
            print("\n🎉 포터블 빌드 완료!")
            print("📁 FlaskSNS_Portable 폴더에 포터블 버전이 생성되었습니다.")
            print("💾 이 폴더를 USB에 복사하여 어디서든 실행할 수 있습니다.")
            
            # 정리
            cleanup()
        else:
            print("❌ 포터블 패키지 생성 실패")
    else:
        print("❌ 빌드 실패")

if __name__ == "__main__":
    main() 