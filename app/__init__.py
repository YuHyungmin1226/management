from __future__ import annotations

import os
from flask import Flask

from .extensions import db, csrf, migrate, limiter
from .config import Config, TestingConfig, DevelopmentConfig, ProductionConfig
from .models import Student, Evaluation  # noqa: F401  # 모델 등록을 위해 import 유지


def create_app(config_name: str | None = None) -> Flask:
    app = Flask(__name__)

    # 설정 로드
    env_config = (config_name or os.environ.get('FLASK_CONFIG') or 'development').lower()
    if env_config == 'production':
        app.config.from_object(ProductionConfig())
    elif env_config == 'testing':
        app.config.from_object(TestingConfig())
    else:
        app.config.from_object(DevelopmentConfig())

    # 확장 초기화
    db.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)

    # 블루프린트 등록
    from .routes_students import bp as students_bp
    from .routes_evaluations import bp as evaluations_bp

    app.register_blueprint(students_bp)
    app.register_blueprint(evaluations_bp)

    # 에러 핸들러
    register_error_handlers(app)

    # 최초 실행 시 DB 생성(개발 용도)
    with app.app_context():
        db.create_all()

    return app


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(404)
    def not_found(error):  # noqa: ANN001
        return (app.render_template('404.html'), 404) if hasattr(app, 'render_template') else ("Not Found", 404)

    @app.errorhandler(500)
    def server_error(error):  # noqa: ANN001
        return (app.render_template('500.html'), 500) if hasattr(app, 'render_template') else ("Server Error", 500)


