#!/bin/bash

# AWS EC2 간단 배포 스크립트
echo "🚀 AWS EC2 간단 배포 시작..."

# 필수 패키지 설치
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv nginx

# 프로젝트 디렉토리 설정
mkdir -p ~/student-management
cd ~/student-management

# 가상환경 설정
python3 -m venv venv
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
export FLASK_ENV=production
export SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')

# 백그라운드에서 애플리케이션 실행
nohup python management_app.py > app.log 2>&1 &

# Nginx 프록시 설정
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

echo "✅ 간단 배포 완료!"
echo "🌐 웹사이트: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)"
echo "📝 로그 확인: tail -f app.log"
