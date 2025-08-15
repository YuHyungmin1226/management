import os
import sys

class Config:
    """기본 설정 클래스"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-this-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = False
    
    # 포터블 버전 대응 - 데이터베이스 경로 설정
    if getattr(sys, 'frozen', False):
        # PyInstaller로 빌드된 경우
        current_dir = os.path.dirname(sys.executable)
    else:
        # 일반 Python 실행의 경우
        current_dir = os.path.dirname(os.path.abspath(__file__))
    
    db_path = os.path.join(current_dir, 'management.db')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_path}'
    
    # 요청 제한 설정
    RATELIMIT_STORAGE_URI = os.environ.get("RATELIMIT_STORAGE_URI", "memory://")
    
    # 파일 업로드 설정
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    
    # 로깅 설정
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = 'management.log'

class DevelopmentConfig(Config):
    """개발 환경 설정"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """운영 환경 설정"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True

class TestingConfig(Config):
    """테스트 환경 설정"""
    TESTING = True
    WTF_CSRF_ENABLED = False
    RATELIMIT_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# 설정 매핑
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
