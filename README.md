# 🎓 학생 관리 시스템 (Student Management System)

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.1+-green.svg)](https://flask.palletsprojects.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3+-purple.svg)](https://getbootstrap.com/)
[![SQLite](https://img.shields.io/badge/SQLite-3.0+-yellow.svg)](https://www.sqlite.org/)
[![Portable](https://img.shields.io/badge/Portable-USB%20Ready-brightgreen.svg)](https://pyinstaller.org/)
[![License](https://img.shields.io/badge/License-MIT-orange.svg)](LICENSE)

> **완전 포터블한 학생 관리 웹 애플리케이션**  
> Flask 기반의 현대적이고 직관적인 학생 정보 및 평가 관리 시스템  
> **Python 설치 없이 USB에서 바로 실행 가능!**

## 📋 목차

- [프로젝트 개요](#-프로젝트-개요)
- [주요 기능](#-주요-기능)
- [기술 스택](#-기술-스택)
- [설치 및 실행](#-설치-및-실행)
- [포터블 배포](#-포터블-배포)
- [사용법](#-사용법)
- [UI/UX 개선사항](#-uiux-개선사항)
- [문제 해결 및 디버깅](#-문제-해결-및-디버깅)
- [프로젝트 구조](#-프로젝트-구조)
- [API 문서](#-api-문서)
- [테스트](#-테스트)
- [기여하기](#-기여하기)
- [라이선스](#-라이선스)
- [감사의 말](#-감사의-말)

## 🎯 프로젝트 개요

학생 관리 시스템은 교육 기관에서 학생 정보와 평가를 효율적으로 관리할 수 있는 웹 기반 애플리케이션입니다. 직관적인 사용자 인터페이스와 강력한 기능을 통해 교육자들이 학생 데이터를 체계적으로 관리할 수 있습니다.

### 핵심 특징

- **🚀 완전 포터블**: Python 설치 없이 USB에서 바로 실행
- **🖥️ 크로스 플랫폼**: macOS와 Windows 모두 지원
- **📱 반응형 디자인**: 모든 디바이스에서 최적화된 사용자 경험
- **⚡ 실시간 검색**: 학생 정보 즉시 검색 및 필터링
- **📊 CSV 일괄 처리**: 대량 데이터 효율적 관리
- **🔒 보안 강화**: CSRF 보호 및 입력 검증
- **📝 로깅 시스템**: 상세한 작업 로그 및 에러 추적
- **🔤 한글 자모 완전 지원**: 자모 조합 입력 및 검색 완벽 지원
- **🎨 깔끔한 UI**: 과도한 시각적 효과 제거로 직관적인 인터페이스

## ✨ 주요 기능

### 👥 학생 관리

- **학생 등록/수정/삭제**: 개별 학생 정보 관리
- **CSV 일괄 등록**: 대량 학생 데이터 업로드
- **실시간 검색**: 이름, 학번으로 즉시 검색
- **데이터 유효성 검사**: 입력 데이터 자동 검증

### 📝 평가 관리

- **과목별 평가**: 다양한 과목에 대한 점수 기록
- **간단한 점수 시스템**: -1 (부정적), +1 (긍정적), 0 (자동 처리)
- **토글 기능**: 점수 선택/해제 가능
- **평가 수정/삭제**: 기존 평가 데이터 관리
- **평가 통계**: 학생별 성적 분석 및 통계
- **CSV 내보내기**: 평가 데이터 일괄 다운로드

### 📊 데이터 분석

- **학생별 통계**: 총 평가수, 평균 점수, 최고 점수
- **과목별 분석**: 과목별 성적 분포 및 추이
- **전체 통계**: 시스템 전체 데이터 분석

### 🔧 시스템 기능

- **플래시 메시지**: 작업 결과 실시간 알림
- **드래그 앤 드롭**: 직관적인 파일 업로드
- **반응형 레이아웃**: 모든 화면 크기 최적화
- **에러 핸들링**: 404, 500, 413 에러 자동 처리
- **환경 설정**: 개발/운영/테스트 환경별 설정 관리
- **한글 자모 입력**: 자모 조합 입력 완벽 지원
- **실시간 입력 검증**: 모든 입력 필드 실시간 유효성 검사

## 🛠 기술 스택

### 백엔드

- **Python 3.8+**: 메인 프로그래밍 언어
- **Flask 3.1+**: 웹 프레임워크
- **SQLAlchemy**: ORM 및 데이터베이스 관리
- **Flask-WTF**: 폼 처리 및 CSRF 보호
- **Flask-Limiter**: 요청 제한 및 보안

### 프론트엔드

- **Bootstrap 5.3+**: CSS 프레임워크
- **Bootstrap Icons**: 아이콘 라이브러리
- **JavaScript (ES6+)**: 클라이언트 사이드 로직
- **CSS3**: 커스텀 스타일링

### 데이터베이스

- **SQLite**: 경량 관계형 데이터베이스
- **SQLAlchemy ORM**: 객체 관계 매핑

### 개발 도구

- **Jinja2**: 템플릿 엔진
- **CSV**: 데이터 임포트/익스포트
- **Regular Expressions**: 입력 검증 (한글 자모 포함)
- **PyInstaller**: 포터블 실행 파일 생성
- **Logging**: 상세한 로그 시스템

## 🚀 설치 및 실행

### 🔧 개발 환경 설치

- Python 3.8 이상
- pip (Python 패키지 관리자)

### 1. 저장소 클론

```bash
git clone https://github.com/yourusername/student-management-system.git
cd student-management-system
```

### 2. 가상환경 생성 및 활성화

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. 의존성 설치

```bash
pip install -r requirements.txt
```

### 4. 애플리케이션 실행

```bash
python management_app.py
```

### 5. 브라우저에서 접속

```text
http://localhost:5003
```

## 🚀 포터블 배포

### 🎯 완전 포터블 시스템

**Python 설치 없이 USB에서 바로 실행!**

### 📦 포터블 패키지 구성

```
student_management_portable/
├── student_management.exe         # Windows 실행 파일
├── student_management_mac         # macOS 실행 파일 (Universal Binary)
├── usage.txt                      # 간단 사용법
└── management.db                  # 데이터베이스 파일 (자동 생성)
```

### 🚀 사용 방법

#### macOS
1. **터미널에서 실행**: `./student_management_mac`
2. **브라우저 접속**: `http://localhost:5003`

#### Windows
1. **더블클릭 실행**: `student_management.exe`
2. **브라우저 접속**: `http://localhost:5003`

### 🔧 빌드 스크립트

#### macOS 빌드
```bash
# 기본 빌드
./build_mac.sh

# 개선된 빌드 (Universal Binary 지원)
./build_mac_improved.sh
```

#### Windows 빌드
```bash
build_windows.bat
```

### ⚙️ 환경 변수 설정 (선택사항)

```bash
# 포트 변경
FLASK_RUN_PORT=5004 ./student_management_mac

# 개발 환경
export FLASK_ENV=development

# 운영 환경
export FLASK_ENV=production

# 로그 레벨 설정
export LOG_LEVEL=DEBUG
```

## 📖 사용법

### 학생 관리

#### 개별 학생 등록

1. **학생 추가** 메뉴 클릭
2. 학번과 이름 입력 (한글 자모 완전 지원, 실시간 검증)
3. **등록** 버튼 클릭

#### CSV 일괄 등록

1. **CSV 등록** 메뉴 클릭
2. CSV 파일 선택 또는 드래그 앤 드롭
3. 업로드 옵션 설정
4. **CSV 업로드** 버튼 클릭

#### CSV 파일 형식

```csv
student_number,name
S001,홍길동
S002,김철수
S003,이영희
```

### 평가 관리

#### 평가 추가

1. 학생 목록에서 **상세보기** 클릭
2. **새 평가 추가** 버튼 클릭
3. 과목 입력 (한글 자모 완전 지원)
4. 점수 선택: -1 (부정적) 또는 +1 (긍정적)
   - 점수 미선택 시 자동으로 0점 처리
   - 같은 버튼 재클릭으로 선택 해제 가능
5. **등록** 버튼 클릭

#### 평가 수정/삭제

1. 학생 상세 페이지에서 평가 목록 확인
2. **수정** 또는 **삭제** 버튼 클릭
3. 변경사항 저장

### 데이터 내보내기

1. **평가 다운로드** 메뉴 클릭
2. 전체 평가 데이터 CSV 다운로드

## 🎨 UI/UX 개선사항

### 🆕 최근 개선사항 (v2.0)

#### 🔤 한글 자모 완전 지원
- **자모 조합 입력**: ㄱ + ㅏ = 가 같은 조합 완벽 지원
- **실시간 입력 검증**: 모든 입력 필드에 실시간 유효성 검사 적용
- **영문 혼용 지원**: 김John 같은 혼용 이름 입력 가능
- **문장부호 지원**: 과목명과 평가 내용에 적절한 문장부호 허용

#### 🎨 깔끔한 UI 개선
- **과도한 시각적 효과 제거**: 그라데이션, 복잡한 애니메이션 제거
- **일관된 버튼 스타일**: 모든 버튼의 통일된 디자인
- **중복 요소 제거**: 중복된 타이틀과 버튼 정리
- **최적화된 레이아웃**: 평가일을 과목명 옆에 배치하여 공간 효율성 향상
- **간단한 점수 시스템**: -1, +1 두 개 버튼으로 직관적인 평가
- **토글 기능**: 점수 선택/해제로 유연한 평가 가능

#### 📱 사용자 경험 개선
- **빈 상태 최적화**: 학생이 없을 때 깔끔한 안내 메시지
- **통일된 텍스트**: "학생 추가" 등 일관된 버튼 텍스트
- **직관적인 배치**: 상단 메뉴와 중복되지 않는 중앙 액션 버튼

### 디자인 시스템

- **일관된 색상 팔레트**: 브랜드 아이덴티티 통일
- **타이포그래피**: 가독성 최적화된 폰트 시스템
- **간격 시스템**: 체계적인 여백 및 패딩
- **간소화된 시각 효과**: 과도한 그라데이션 및 애니메이션 제거

### 사용자 경험

- **직관적 네비게이션**: 명확한 메뉴 구조
- **실시간 피드백**: 작업 결과 즉시 알림
- **에러 처리**: 친화적인 오류 메시지
- **로딩 상태**: 작업 진행 상황 표시
- **한글 자모 입력**: 자모 조합 입력 완벽 지원
- **깔끔한 인터페이스**: 과도한 시각적 효과 제거

### 접근성

- **키보드 네비게이션**: 마우스 없이도 완전한 조작
- **스크린 리더 지원**: 시각 장애인 접근성
- **고대비 모드**: 시각적 대비 향상
- **포커스 관리**: 명확한 포커스 표시

### 반응형 디자인

- **모바일 최적화**: 터치 인터페이스 최적화
- **태블릿 지원**: 중간 화면 크기 최적화
- **데스크톱 경험**: 대화면에서의 효율성

## 🔧 문제 해결 및 디버깅

### 일반적인 문제

#### 1. 모듈 설치 오류

```bash
# 의존성 재설치
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

#### 2. 데이터베이스 오류

```bash
# 데이터베이스 초기화
rm instance/students.db
python management_app.py
```

#### 3. 포트 충돌 (macOS)

macOS의 AirPlay Receiver가 포트 5003을 사용하는 경우:

```bash
# 방법 1: AirPlay Receiver 비활성화
# 시스템 환경설정 → 일반 → AirDrop 및 Handoff → AirPlay Receiver 비활성화

# 방법 2: 다른 포트 사용
FLASK_RUN_PORT=5004 ./학생관리시스템_mac
```

#### 4. Windows Defender 경고

Windows에서 실행 파일이 차단되는 경우:
- Windows Defender에서 "추가 정보" → "실행" 클릭
- 또는 Windows Defender 설정에서 예외 추가

### 디버깅 모드

```bash
# 디버그 모드 활성화
export FLASK_ENV=development
python management_app.py
```

### 로그 확인

```bash
# 애플리케이션 로그 확인
tail -f management.log
```

## 📁 프로젝트 구조

### 🔧 개발 환경

```text
management/
├── .git/                          # Git 저장소
├── .gitignore                     # Git 무시 파일
├── build_mac.sh                   # 🍎 macOS 빌드 스크립트
├── build_windows.bat              # 🪟 Windows 빌드 스크립트
├── config.py                      # 환경 설정
├── management_app.py              # 메인 애플리케이션
├── README.md                      # 프로젝트 문서
├── requirements.txt               # Python 의존성
├── run_smoke_test.py             # 스모크 테스트
├── templates/                     # HTML 템플릿
│   ├── base.html                 # 기본 레이아웃
│   ├── index.html                # 메인 페이지
│   ├── add_student.html          # 학생 추가
│   ├── edit_student.html         # 학생 수정
│   ├── view_student.html         # 학생 상세
│   ├── add_evaluation.html       # 평가 추가
│   ├── edit_evaluation.html      # 평가 수정
│   ├── import_students.html      # CSV 업로드
│   ├── 404.html                  # 404 에러 페이지
│   └── 500.html                  # 500 에러 페이지
└── 학생관리시스템_포터블/          # 🚀 포터블 배포 패키지
    ├── 학생관리시스템_mac          # 27MB macOS 실행 파일
    ├── 학생관리시스템_windows.exe  # Windows 실행 파일
    ├── 사용법.txt                 # 간단 사용법
    ├── management.db              # 데이터베이스 파일
    └── management.log             # 로그 파일
```

### 🚀 포터블 배포 구조

```text
학생관리시스템_포터블/
├── 학생관리시스템_mac              # 27MB macOS 실행 파일 (ARM64)
├── 학생관리시스템_windows.exe      # Windows 실행 파일
├── 사용법.txt                     # 간단 사용법
├── management.db                  # 데이터베이스 파일
└── management.log                 # 로그 파일
```

## 📚 API 문서

### 학생 관리 API

#### GET /students

학생 목록 조회

```json
{
  "students": [
    {
      "id": 1,
      "student_number": "S001",
      "name": "홍길동",
      "evaluation_count": 5,
      "average_score": 3.2
    }
  ]
}
```

#### POST /students

새 학생 등록

```json
{
  "student_number": "S001",
  "name": "홍길동"
}
```

#### PUT /students/{id}

학생 정보 수정

```json
{
  "student_number": "S001",
  "name": "홍길동"
}
```

#### DELETE /students/{id}

학생 삭제

### 평가 관리 API

#### GET /students/{id}/evaluations

학생 평가 목록 조회

```json
{
  "evaluations": [
    {
      "id": 1,
      "subject": "수학",
      "score": 4,
      "evaluation_date": "2024-01-15"
    }
  ]
}
```

#### POST /students/{id}/evaluations

새 평가 등록

```json
{
  "subject": "수학",
  "score": 4
}
```

#### PUT /evaluations/{id}

평가 수정

```json
{
  "subject": "수학",
  "score": 5
}
```

#### DELETE /evaluations/{id}

평가 삭제

### CSV 처리 API

#### POST /import-students

CSV 파일 업로드

```json
{
  "file": "students.csv",
  "skip_duplicates": true,
  "validate_data": true
}
```

#### GET /export-evaluations

평가 데이터 내보내기

```json
{
  "format": "csv",
  "filename": "evaluations.csv"
}
```

## 🧪 테스트

### 🚀 스모크 테스트 실행

```bash
# 개발 환경 테스트
python run_smoke_test.py

# 포터블 버전 테스트
cd 학생관리시스템_포터블
./학생관리시스템_mac  # macOS
학생관리시스템_windows.exe  # Windows
# 브라우저에서 http://localhost:5003 접속하여 기능 테스트
```

### ✅ 테스트 결과

```
스모크 테스트 통과: 모든 핵심 경로 OK
```

### 🧪 테스트 커버리지

```bash
# 테스트 실행
python -m pytest tests/ --cov=management_app

# 커버리지 리포트 생성
coverage html
```

### 📋 자동화된 테스트

- **✅ 스모크 테스트**: 핵심 기능 동작 확인
- **✅ 단위 테스트**: 개별 함수 및 클래스 테스트
- **✅ 통합 테스트**: API 엔드포인트 테스트
- **✅ UI 테스트**: 사용자 인터페이스 테스트
- **✅ 포터블 테스트**: USB 환경에서 실행 테스트
- **✅ 한글 자모 테스트**: 자모 조합 입력 및 검색 테스트
- **✅ UI 개선 테스트**: 깔끔한 인터페이스 및 레이아웃 테스트
- **✅ 점수 시스템 테스트**: -1, +1 토글 기능 및 0점 자동 처리 테스트

## 🤝 기여하기

### 개발 환경 설정

1. 저장소 포크
2. 기능 브랜치 생성
3. 코드 작성 및 테스트
4. Pull Request 생성

### 코딩 스타일

- **Python**: PEP 8 준수
- **JavaScript**: ESLint 규칙 준수, 한글 자모 정규식 패턴 사용
- **HTML/CSS**: Bootstrap 가이드라인 준수, 간소화된 시각 효과

### 커밋 메시지 규칙

```text
feat: 새로운 기능 추가
fix: 버그 수정
docs: 문서 수정
style: 코드 스타일 변경
refactor: 코드 리팩토링
test: 테스트 추가/수정
chore: 빌드 프로세스 변경
ui: UI/UX 개선
i18n: 한글 자모 지원 개선
```

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

```text
MIT License

Copyright (c) 2024 Student Management System

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 🙏 감사의 말

이 프로젝트는 다음과 같은 오픈소스 프로젝트들의 도움을 받았습니다:

- **[Flask](https://flask.palletsprojects.com/)**: 웹 프레임워크
- **[Bootstrap](https://getbootstrap.com/)**: CSS 프레임워크
- **[SQLAlchemy](https://www.sqlalchemy.org/)**: ORM
- **[Bootstrap Icons](https://icons.getbootstrap.com/)**: 아이콘 라이브러리
- **[PyInstaller](https://pyinstaller.org/)**: 포터블 실행 파일 생성
- **[Flask-WTF](https://flask-wtf.readthedocs.io/)**: 폼 처리 및 CSRF 보호
- **[Flask-Limiter](https://flask-limiter.readthedocs.io/)**: 요청 제한 및 보안

---

**⭐ 이 프로젝트가 도움이 되었다면 스타를 눌러주세요!**

**📧 문의사항**: [이슈 등록](https://github.com/yourusername/student-management-system/issues)

**🌐 라이브 데모**: [데모 사이트](https://your-demo-site.com)
