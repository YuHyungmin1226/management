# Flask SNS 포터블 앱 🚀

USB에 복사하여 어디서든 실행할 수 있는 개인 SNS 애플리케이션입니다.

## ✨ 주요 기능

- **개인 SNS**: 나만의 소셜 네트워크 서비스
- **파일 첨부**: 이미지, 비디오, 문서, 오디오 파일 업로드
- **URL 미리보기**: 링크 공유 시 자동 미리보기 생성
- **댓글 시스템**: 게시물에 댓글 작성
- **사용자 관리**: 계정 생성, 비밀번호 변경
- **포터블**: USB에 복사하여 어디서든 실행

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

### 3. USB 사용

1. 이 폴더 전체를 USB에 복사
2. USB를 다른 PC에 연결
3. `FlaskSNS.py` 실행
4. 브라우저에서 접속

## 📁 폴더 구조

```
FlaskSNS/
├── FlaskSNS.py          # 메인 실행 파일
├── app.py              # Flask 애플리케이션
├── requirements.txt    # Python 패키지 목록
├── templates/          # HTML 템플릿
├── utils/             # 유틸리티 함수
├── sns.db             # 데이터베이스 (자동 생성)
├── uploads/           # 업로드 파일 (자동 생성)
└── README.md          # 이 파일
```

## 💾 데이터 저장

모든 데이터는 실행 파일과 같은 폴더에 저장됩니다:

- **데이터베이스**: `sns.db` (계정, 게시물, 댓글)
- **업로드 파일**: `uploads/` 폴더
  - `images/` - 이미지 파일
  - `videos/` - 비디오 파일
  - `documents/` - 문서 파일
  - `audio/` - 오디오 파일
  - `archives/` - 압축 파일

## 🔧 시스템 요구사항

- **OS**: Windows 10/11, macOS, Linux
- **Python**: 3.8 이상
- **메모리**: 최소 512MB
- **저장공간**: 최소 100MB

## 📦 필요한 패키지

```bash
pip install -r requirements.txt
```

### 주요 패키지
- Flask - 웹 프레임워크
- Flask-SQLAlchemy - 데이터베이스 ORM
- Flask-Login - 사용자 인증
- Pillow - 이미지 처리
- filetype - 파일 타입 감지
- requests - HTTP 요청
- BeautifulSoup4 - 웹 스크래핑

## 🛡️ 보안

- **기본 비밀번호**: 첫 실행 시 admin/admin123
- **비밀번호 변경**: 로그인 후 프로필에서 변경 권장
- **데이터 보호**: 모든 데이터는 로컬에만 저장

## 🔄 업데이트

1. 기존 폴더 백업
2. 새 버전 다운로드
3. 기존 `sns.db`와 `uploads/` 폴더 복사
4. 새 버전 실행

## 🐛 문제 해결

### 포트 충돌
- 다른 포트 사용 중인 경우 자동으로 다른 포트 선택

### 파일 업로드 실패
- 파일 크기 제한: 10MB
- 지원 형식 확인

### 데이터베이스 오류
- `sns.db` 파일 삭제 후 재실행
- 백업 데이터 복원

## 📞 지원

문제가 있으면 GitHub 이슈를 생성해주세요.

## 📄 라이선스

MIT License

---

**Flask SNS 포터블 앱** - 나만의 소셜 네트워크를 USB에 담아가세요! 💾✨ 