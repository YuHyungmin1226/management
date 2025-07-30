# Flask SNS 포터블 앱 🚀

USB에 복사하여 어디서든 실행할 수 있는 개인 SNS 애플리케이션입니다.

## ✨ 주요 기능

- **개인 SNS**: 나만의 소셜 네트워크 서비스
- **파일 첨부**: 이미지, 비디오, 문서, 오디오 파일 업로드 (최대 10MB)
- **URL 미리보기**: 링크 공유 시 자동 미리보기 생성 (YouTube 특별 지원)
- **댓글 시스템**: 게시물에 댓글 작성
- **사용자 관리**: 계정 생성, 비밀번호 변경, 관리자 기능
- **포터블**: USB에 복사하여 어디서든 실행
- **한국 시간 지원**: KST 시간대 적용
- **보안 기능**: 로그인 시도 제한, 계정 잠금

## 🚀 시작하기

### 1. 실행 방법

```bash
# Python이 설치된 경우
python FlaskSNS.py

# 또는 더블클릭으로 실행
FlaskSNS.py
```

### 2. 접속

- **URL**: http://localhost:5001
- **기본 계정**: admin / admin123
- **네트워크 접속**: http://[IP주소]:5001 (같은 네트워크 내에서)

### 3. USB 사용

1. 이 폴더 전체를 USB에 복사
2. USB를 다른 PC에 연결
3. `FlaskSNS.py` 실행
4. 브라우저에서 접속

## 📁 폴더 구조

```
FlaskSNS/
├── FlaskSNS.py          # 메인 실행 파일
├── app.py              # Flask 애플리케이션 (598줄)
├── requirements.txt    # Python 패키지 목록
├── templates/          # HTML 템플릿 (9개 파일)
│   ├── base.html      # 기본 템플릿
│   ├── index.html     # 메인 페이지
│   ├── login.html     # 로그인 페이지
│   ├── register.html  # 회원가입 페이지
│   ├── new_post.html  # 새 게시물 작성
│   ├── view_post.html # 게시물 보기
│   ├── profile.html   # 프로필 페이지
│   ├── admin.html     # 관리자 페이지
│   └── change_password.html # 비밀번호 변경
├── utils/             # 유틸리티 함수
│   ├── url_utils.py   # URL 미리보기 생성
│   └── file_utils.py  # 파일 처리 유틸리티
├── sns.db             # 데이터베이스 (자동 생성)
├── uploads/           # 업로드 파일 (자동 생성)
└── README.md          # 이 파일
```

## 💾 데이터 저장

모든 데이터는 실행 파일과 같은 폴더에 저장됩니다:

- **데이터베이스**: `sns.db` (계정, 게시물, 댓글) - 자동 생성
- **업로드 파일**: `uploads/` 폴더 - 자동 생성
  - `images/` - 이미지 파일 (PNG, JPG, GIF, WebP, BMP)
  - `videos/` - 비디오 파일 (MP4, AVI, MOV, WMV, FLV, MKV)
  - `documents/` - 문서 파일 (PDF, DOC, DOCX, TXT, RTF)
  - `audio/` - 오디오 파일 (MP3, WAV, FLAC, OGG, M4A)
  - `archives/` - 압축 파일 (ZIP, RAR, 7Z, TAR, GZ)

### 🔄 데이터 백업 및 복원

**백업 방법:**
1. `sns.db` 파일 복사
2. `uploads/` 폴더 전체 복사

**복원 방법:**
1. 백업한 `sns.db` 파일을 앱 폴더에 복사
2. 백업한 `uploads/` 폴더를 앱 폴더에 복사
3. 앱 재실행

**⚠️ 주의사항:**
- `sns.db`와 `uploads/` 폴더는 Git에 포함되지 않습니다
- 각 사용자마다 고유한 데이터베이스가 생성됩니다
- 데이터 백업은 정기적으로 수행하세요

## 🔧 시스템 요구사항

- **OS**: Windows 10/11, macOS, Linux
- **Python**: 3.8 이상 (3.13에서 테스트 완료)
- **메모리**: 최소 512MB
- **저장공간**: 최소 100MB
- **네트워크**: 로컬 네트워크 접속 지원

## 📦 필요한 패키지

```bash
pip install -r requirements.txt
```

### 주요 패키지 (2025년 7월 기준)
- **Flask 2.3.3** - 웹 프레임워크
- **Flask-SQLAlchemy 3.0.5** - 데이터베이스 ORM
- **Flask-Login 0.6.3** - 사용자 인증
- **Pillow 11.3.0** - 이미지 처리
- **filetype 1.2.0** - 파일 타입 감지
- **python-magic-bin 0.4.14** - 파일 매직 넘버 감지
- **requests 2.31.0** - HTTP 요청
- **beautifulsoup4 4.12.2** - 웹 스크래핑
- **waitress 3.0.2** - 프로덕션 WSGI 서버
- **WTForms 3.0.1** - 폼 처리
- **SQLAlchemy 2.0.41** - 데이터베이스 툴킷

## 🛡️ 보안

- **기본 비밀번호**: 첫 실행 시 admin/admin123
- **비밀번호 변경**: 로그인 후 프로필에서 변경 권장
- **데이터 보호**: 모든 데이터는 로컬에만 저장
- **로그인 제한**: 5회 실패 시 15분 계정 잠금
- **파일 검증**: 업로드 파일 타입 및 크기 검증

## 🔄 업데이트

1. 기존 폴더 백업
2. 새 버전 다운로드
3. 기존 `sns.db`와 `uploads/` 폴더 복사
4. 새 버전 실행

## 🐛 문제 해결

### 포트 충돌
- 기본 포트 5001 사용
- 다른 포트 사용 중인 경우 자동으로 다른 포트 선택

### 파일 업로드 실패
- 파일 크기 제한: 10MB
- 지원 형식 확인
- 파일 타입 자동 감지

### 데이터베이스 오류
- `sns.db` 파일 삭제 후 재실행
- 백업 데이터 복원

### Python 버전 호환성
- Python 3.8 이상 지원
- Python 3.13에서 테스트 완료

## 🌟 새로운 기능

### v2.0 업데이트 (2025년 7월)
- ✅ Python 3.13 호환성 개선
- ✅ Pillow 11.3.0 업데이트
- ✅ filetype 패키지 추가로 파일 타입 감지 개선
- ✅ python-magic-bin으로 Windows 호환성 향상
- ✅ waitress 3.0.2로 프로덕션 서버 성능 개선
- ✅ 네트워크 접속 지원 (같은 네트워크 내에서)
- ✅ 한국 시간대 지원 개선

## 📞 지원

문제가 있으면 GitHub 이슈를 생성해주세요.

## 📄 라이선스

MIT License

---

**Flask SNS 포터블 앱** - 나만의 소셜 네트워크를 USB에 담아가세요! 💾✨ 