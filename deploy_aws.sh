#!/bin/bash

# AWS EC2 배포 스크립트
echo "🚀 AWS EC2 배포 시작..."

# 시스템 업데이트
echo "📦 시스템 패키지 업데이트..."
sudo apt-get update
sudo apt-get upgrade -y

# Python 및 pip 설치
echo "🐍 Python 설치..."
sudo apt-get install -y python3 python3-pip python3-venv

# Git 설치
echo "📥 Git 설치..."
sudo apt-get install -y git

# 프로젝트 디렉토리 생성
echo "📁 프로젝트 디렉토리 설정..."
mkdir -p /home/ubuntu/student-management
cd /home/ubuntu/student-management

# 가상환경 생성 및 활성화
echo "🔧 가상환경 설정..."
python3 -m venv venv
source venv/bin/activate

# 의존성 설치
echo "📦 Python 패키지 설치..."
pip install --upgrade pip
pip install -r requirements.txt

# 환경 변수 설정
echo "⚙️ 환경 변수 설정..."
export FLASK_ENV=production
export SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')

# 서비스 파일 생성
echo "🔧 시스템 서비스 설정..."
sudo tee /etc/systemd/system/student-management.service > /dev/null <<EOF
[Unit]
Description=Student Management System
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/student-management
Environment=PATH=/home/ubuntu/student-management/venv/bin
Environment=FLASK_ENV=production
Environment=SECRET_KEY=$SECRET_KEY
ExecStart=/home/ubuntu/student-management/venv/bin/python management_app.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# 서비스 활성화 및 시작
echo "🚀 서비스 시작..."
sudo systemctl daemon-reload
sudo systemctl enable student-management
sudo systemctl start student-management

# Nginx 설치 및 설정
echo "🌐 Nginx 설정..."
sudo apt-get install -y nginx

sudo tee /etc/nginx/sites-available/student-management > /dev/null <<EOF
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:5003;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Nginx 설정 활성화
sudo ln -sf /etc/nginx/sites-available/student-management /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo systemctl restart nginx

echo "✅ 배포 완료!"
echo "🌐 웹사이트: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)"
echo "📝 로그 확인: sudo journalctl -u student-management -f"
