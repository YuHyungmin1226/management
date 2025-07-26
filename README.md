# Flask SNS 애플리케이션

Flask로 개발된 소셜 네트워킹 서비스(SNS) 애플리케이션입니다. 사용자들이 게시물을 작성하고, 댓글을 달며, 파일을 업로드할 수 있는 웹 애플리케이션입니다.

## 🚀 주요 기능

- **사용자 관리**
  - 회원가입 및 로그인
  - 비밀번호 변경
  - 계정 잠금 기능 (보안)
  - 프로필 관리

- **게시물 관리**
  - 게시물 작성 및 수정
  - 게시물 삭제
  - 댓글 작성
  - URL 미리보기 기능

- **파일 업로드**
  - 이미지 및 문서 파일 업로드
  - 파일 다운로드
  - 파일 삭제

- **관리자 기능**
  - 사용자 관리
  - 시스템 모니터링

## 🛠️ 기술 스택

- **Backend**: Flask 2.3.3
- **Database**: SQLite (Flask-SQLAlchemy)
- **Authentication**: Flask-Login
- **File Handling**: Pillow, python-magic
- **Web Scraping**: BeautifulSoup4 (URL 미리보기)
- **Production Server**: Waitress

## 📋 설치 및 실행

### 1. 저장소 클론
```bash
git clone <repository-url>
cd flask_sns_app
```

### 2. 가상환경 생성 및 활성화 (선택사항)
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
# 가상환경을 사용하는 경우
pip install -r requirements.txt

# 가상환경을 사용하지 않는 경우 (시스템에 직접 설치)
pip install Flask Flask-SQLAlchemy Flask-Login Flask-WTF WTForms Werkzeug requests beautifulsoup4 python-dotenv Pillow waitress filetype
```

### 4. 환경 변수 설정 (선택사항)
```bash
# .env 파일 생성
SECRET_KEY=your-secret-key-here
```

### 5. 데이터베이스 초기화
```bash
python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
>>> exit()
```

### 6. 애플리케이션 실행
```bash
python app.py
```

애플리케이션이 `http://localhost:5000`에서 실행됩니다.

## 📁 프로젝트 구조

```
flask_sns_app/
├── app.py                 # 메인 애플리케이션 파일
├── run.py                 # 실행 스크립트
├── requirements.txt       # Python 의존성
├── config/               # 설정 파일
├── templates/            # HTML 템플릿
│   ├── base.html         # 기본 템플릿
│   ├── index.html        # 메인 페이지
│   ├── login.html        # 로그인 페이지
│   ├── register.html     # 회원가입 페이지
│   ├── new_post.html     # 게시물 작성 페이지
│   ├── view_post.html    # 게시물 보기 페이지
│   ├── profile.html      # 프로필 페이지
│   ├── admin.html        # 관리자 페이지
│   └── change_password.html # 비밀번호 변경 페이지
└── utils/                # 유틸리티 함수
    ├── file_utils.py     # 파일 처리 유틸리티
    └── url_utils.py      # URL 미리보기 유틸리티
```

## 🔧 주요 라우트

- `/` - 메인 페이지 (로그인 후 게시물 목록)
- `/login` - 로그인
- `/register` - 회원가입
- `/logout` - 로그아웃
- `/post/new` - 새 게시물 작성
- `/post/<id>` - 게시물 보기
- `/profile` - 사용자 프로필
- `/admin` - 관리자 페이지
- `/change_password` - 비밀번호 변경

## 🔒 보안 기능

- 비밀번호 해싱 (Werkzeug)
- 계정 잠금 기능 (로그인 실패 시)
- 세션 관리
- 파일 업로드 검증

## 📝 API 엔드포인트

- `GET /api/posts` - 게시물 목록 (JSON)

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 📞 문의

프로젝트에 대한 문의사항이 있으시면 이슈를 생성해 주세요. 