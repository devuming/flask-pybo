from flask import Flask
from flask_migrate import Migrate           # db 관련
from flask_sqlalchemy import SQLAlchemy

import config   # 설정 파일

# 전역변수로 선언
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    # app 객체 생성
    app = Flask(__name__)
    app.config.from_object(config)          # 설정값 가져오기

    # ORM
    db.init_app(app)
    migrate.init_app(app, db)
    from . import models


    '''
    @app.route('/')     # / 에 매핑
    def hello_pybo():
        return 'Hello, Pybo'
    '''
    # blueprint views 모듈(페이지) import
    from .views import main_views, question_views, answer_views, auth_views
    app.register_blueprint(main_views.bp)               # 페이지 동작은 main_views 파일에서 정의
    app.register_blueprint(question_views.bp)           # 페이지 동작은 question_views 파일에서 정의
    app.register_blueprint(answer_views.bp)             # 페이지 동작은 answer_views 파일에서 정의
    app.register_blueprint(auth_views.bp)

    # 필터
    from .filter import format_datetime
    app.jinja_env.filters['datetime'] = format_datetime # 필터 등록
    return app