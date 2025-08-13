from __future__ import annotations

import os
import sys
from datetime import timedelta


def _default_db_path() -> str:
    if getattr(sys, 'frozen', False):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.dirname(os.path.abspath(__file__))
        # app/ 기준에서 상위로 올려 프로젝트 루트에 db 생성
        base = os.path.abspath(os.path.join(base, os.pardir))
    return os.path.join(base, 'management.db')


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'change-this-in-env')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', f'sqlite:///{_default_db_path()}')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 세션/쿠키 보안
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    # Limiter 기본 제한(extensions에서 default 설정도 있으나 여기도 참고로 둠)
    RATELIMIT_DEFAULT = "200/day;50/hour"


class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False


class TestingConfig(Config):
    TESTING = True
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False  # 테스트 편의
    SESSION_COOKIE_SECURE = False


class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True


