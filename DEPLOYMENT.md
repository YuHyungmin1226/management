# 🚀 배포 가이드 (Deployment Guide)

## 📋 목차

- [Railway 배포](#railway-배포)
- [AWS EC2 배포](#aws-ec2-배포)
- [환경 변수 설정](#환경-변수-설정)
- [문제 해결](#문제-해결)

## 🚂 Railway 배포

### 1. Railway 계정 설정

1. [Railway.app](https://railway.app)에 가입
2. GitHub 계정 연결

### 2. 프로젝트 배포

#### 방법 1: GitHub 연동 (권장)

```bash
# 1. GitHub에 코드 푸시
git add .
git commit -m "feat: Railway 배포 준비"
git push origin main

# 2. Railway 대시보드에서 "Deploy from GitHub repo" 클릭
# 3. 저장소 선택 후 배포
```

#### 방법 2: CLI 사용

```bash
# Railway CLI 설치
npm install -g @railway/cli

# 로그인
railway login

# 프로젝트 초기화
railway init

# 배포
railway up
```

### 3. 환경 변수 설정

Railway 대시보드에서 다음 환경 변수 설정:

```bash
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
```

### 4. PostgreSQL 데이터베이스 추가

1. Railway 대시보드에서 "New" → "Database" → "PostgreSQL" 선택
2. 자동으로 `DATABASE_URL` 환경 변수가 설정됨

### 5. 도메인 설정

Railway 대시보드에서 "Settings" → "Domains"에서 커스텀 도메인 설정 가능

## ☁️ AWS EC2 배포

### 1. EC2 인스턴스 생성

1. AWS 콘솔에서 EC2 인스턴스 생성
2. Ubuntu Server 22.04 LTS 선택
3. t2.micro (무료 티어) 선택
4. 보안 그룹 설정:
   - SSH (포트 22)
   - HTTP (포트 80)
   - HTTPS (포트 443)

### 2. SSH 연결

```bash
# 키 파일 권한 설정
chmod 400 your-key.pem

# SSH 연결
ssh -i your-key.pem ubuntu@your-ec2-public-ip
```

### 3. 자동 배포 스크립트 실행

#### 전체 배포 (권장)

```bash
# 스크립트 다운로드
wget https://raw.githubusercontent.com/yourusername/management/main/deploy_aws.sh

# 실행 권한 부여
chmod +x deploy_aws.sh

# 배포 실행
./deploy_aws.sh
```

#### 간단 배포

```bash
# 스크립트 다운로드
wget https://raw.githubusercontent.com/yourusername/management/main/deploy_aws_simple.sh

# 실행 권한 부여
chmod +x deploy_aws_simple.sh

# 배포 실행
./deploy_aws_simple.sh
```

### 4. 수동 배포

```bash
# 시스템 업데이트
sudo apt-get update
sudo apt-get upgrade -y

# Python 설치
sudo apt-get install -y python3 python3-pip python3-venv nginx

# 프로젝트 클론
git clone https://github.com/yourusername/management.git
cd management

# 가상환경 설정
python3 -m venv venv
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
export FLASK_ENV=production
export SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')

# 애플리케이션 실행
nohup python management_app.py > app.log 2>&1 &

# Nginx 설정
sudo tee /etc/nginx/sites-available/student-management > /dev/null <<EOF
server {
    listen 80;
    server_name _;
    location / {
        proxy_pass http://127.0.0.1:5003;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/student-management /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo systemctl restart nginx
```

## ⚙️ 환경 변수 설정

### 필수 환경 변수

```bash
# Flask 환경
FLASK_ENV=production

# 보안 키 (자동 생성 또는 수동 설정)
SECRET_KEY=your-secret-key-here

# 포트 (Railway는 자동 설정)
PORT=5003
```

### 선택적 환경 변수

```bash
# 로그 레벨
LOG_LEVEL=INFO

# 데이터베이스 URL (Railway에서 자동 설정)
DATABASE_URL=postgresql://...
```

## 🔧 문제 해결

### Railway 문제

#### 1. 빌드 실패

```bash
# 로그 확인
railway logs

# 로컬에서 테스트
python management_app.py
```

#### 2. 데이터베이스 연결 오류

```bash
# DATABASE_URL 확인
railway variables

# PostgreSQL 확장 설치 확인
pip install psycopg2-binary
```

### AWS EC2 문제

#### 1. 서비스 시작 실패

```bash
# 서비스 상태 확인
sudo systemctl status student-management

# 로그 확인
sudo journalctl -u student-management -f
```

#### 2. Nginx 오류

```bash
# Nginx 상태 확인
sudo systemctl status nginx

# 설정 파일 문법 검사
sudo nginx -t

# 로그 확인
sudo tail -f /var/log/nginx/error.log
```

#### 3. 포트 충돌

```bash
# 포트 사용 확인
sudo netstat -tlnp | grep :5003

# 프로세스 종료
sudo pkill -f management_app.py
```

### 일반적인 문제

#### 1. 권한 오류

```bash
# 파일 권한 설정
chmod +x deploy_aws.sh
chmod +x deploy_aws_simple.sh

# 디렉토리 권한 설정
sudo chown -R ubuntu:ubuntu ~/student-management
```

#### 2. 메모리 부족

```bash
# 메모리 사용량 확인
free -h

# 스왑 메모리 추가
sudo fallocate -l 1G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

## 📊 모니터링

### Railway 모니터링

- Railway 대시보드에서 실시간 로그 확인
- 메트릭스 및 성능 모니터링
- 자동 스케일링 설정

### AWS EC2 모니터링

```bash
# 시스템 리소스 모니터링
htop

# 애플리케이션 로그
tail -f app.log

# Nginx 액세스 로그
sudo tail -f /var/log/nginx/access.log
```

## 🔄 업데이트

### Railway 업데이트

```bash
# 코드 변경 후 GitHub에 푸시
git add .
git commit -m "feat: 업데이트 내용"
git push origin main

# Railway에서 자동 배포됨
```

### AWS EC2 업데이트

```bash
# 서버에 SSH 연결
ssh -i your-key.pem ubuntu@your-ec2-public-ip

# 프로젝트 업데이트
cd ~/student-management
git pull origin main

# 가상환경 활성화
source venv/bin/activate

# 의존성 업데이트
pip install -r requirements.txt

# 서비스 재시작
sudo systemctl restart student-management
```

## 🛡️ 보안 고려사항

### Railway 보안

- 환경 변수로 민감한 정보 관리
- HTTPS 자동 설정
- 자동 백업 및 복구

### AWS EC2 보안

```bash
# 방화벽 설정
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable

# SSL 인증서 설정 (Let's Encrypt)
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

---

**📧 문의사항**: 배포 중 문제가 발생하면 이슈를 등록해주세요!
