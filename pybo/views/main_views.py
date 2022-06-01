from flask import Blueprint, url_for
from werkzeug.utils import redirect

bp = Blueprint('main', __name__, url_prefix='/')    # 루트

@bp.route('/hello')
def hello_pybo():
    return 'Hello, Pybo!!!!'

@bp.route('/')      # 루트로 들어온 경우
def index():
    return redirect(url_for('question._list'))      # question Blueprint의 list 함수 호출