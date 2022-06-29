from flask import Flask
from flask_migrate import Migrate           # db 관련
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flaskext.markdown import Markdown

import config   # 설정 파일

naming_convention = {
    "ix":"ix_%(column_0_label)s",
    "uq":"uq_%(table_name)s_%(column_0_name)s",
    "ck":"ck_%(table_name)s_%(column_0_name)s",
    "fk":"fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk":"pk_%(table_name)s"
}   # 인덱스 등 제약조건 이름 규칙 정의

# 전역변수로 선언
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()

def create_app():
    # app 객체 생성
    app = Flask(__name__)
    app.config.from_object(config)          # 설정값 가져오기

    # ORM
    db.init_app(app)
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)
    from . import models


    '''
    @app.route('/')     # / 에 매핑
    def hello_pybo():
        return 'Hello, Pybo'
    '''
    # blueprint views 모듈(페이지) import
    from .views import main_views, question_views, answer_views, auth_views, comment_views, vote_views
    app.register_blueprint(main_views.bp)               # 페이지 동작은 main_views 파일에서 정의
    app.register_blueprint(question_views.bp)           # 페이지 동작은 question_views 파일에서 정의
    app.register_blueprint(answer_views.bp)             # 페이지 동작은 answer_views 파일에서 정의
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(comment_views.bp)
    app.register_blueprint(vote_views.bp)

    # 필터
    from .filter import format_datetime
    app.jinja_env.filters['datetime'] = format_datetime # 필터 등록

    # Markdown
    Markdown(app, extensions=['nl2br', 'fenced_code'])      # 게시물에 마크다운 적용

    return app