import os

BASE_DIR = os.path.dirname(__file__)

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False     # 이벤트 처리 옵션

SECRET_KEY = "dev"      # 웹취약점 공격 방지 : 데이터 전달 시 도메인이 같은지 체크