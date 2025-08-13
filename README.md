# 학생 관리 시스템 (Flask)

간단한 학생/평가 관리용 Flask + SQLite 애플리케이션입니다. PyInstaller 등 포터블 실행을 고려해 실행 파일과 동일 폴더에 DB를 생성합니다.

## 주요 기능
- 학생 등록/조회/수정/삭제
- 학생별 평가 기록 추가/삭제
- 점수 범위 검증(0~100), 학번 중복 검증

## 폴더 구조
```
Management/
├── management_app.py        # 메인 Flask 앱
├── requirements.txt         # 의존성
├── templates/               # 템플릿
│   ├── base.html
│   ├── index.html
│   ├── add_student.html
│   ├── edit_student.html
│   ├── view_student.html
│   └── add_evaluation.html
└── run_smoke_test.py        # 스모크 테스트 스크립트
```

## 실행 방법
1) 가상환경 생성 및 패키지 설치
```
python -m venv .venv
./.venv/Scripts/activate  # Windows PowerShell
pip install -r requirements.txt
```

2) 앱 실행
```
python management_app.py
```
브라우저에서 `http://localhost:5000` 접속

## 환경 설정
- `SECRET_KEY`: 환경변수로 주입 권장. 미설정 시 기본값이 사용됩니다.
- DB 경로: 실행 파일과 동일 폴더의 `management.db` (포터블 대응 포함)

## 테스트
간단한 주요 경로 점검용 스모크 테스트 제공:
```
./.venv/Scripts/activate
python run_smoke_test.py
```
인메모리 SQLite를 사용하며 다음을 검증합니다.
- 인덱스 접근, 학생 추가/중복, 상세 조회
- 평가 추가(날짜/점수 형식), 점수 범위 오류, 평가 삭제
- 학생 수정/학번 중복, 학생 삭제

## 권장 사항(보안/운영)
- 운영 시 CSRF 보호(Flask-WTF) 적용 권장
- `debug=False`로 WSGI 서버(waitress, gunicorn 등) 사용 권장
- 마이그레이션 도구(Flask-Migrate) 도입 시 스키마 변경 관리 용이

## 라이선스
MIT License