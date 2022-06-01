from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash  # 비밀번호 암호화 생성
from werkzeug.utils import redirect

from pybo import db
from pybo.forms import UserCreateForm, UserLoginForm
from pybo.models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():              # validation check 여부확인
        user = User.query.filter_by(username=form.username.data).first()    # username의 데이터 가져오기
        if not user:    # db에 같은 username으로 이미 등록된 user가 없으면
            user = User(username=form.username.data,
                        password=generate_password_hash(form.password1.data),
                        email=form.email.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('이미 존재하는 사용자입니다.')

    return render_template('auth/signup.html', form=form)

@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(username=form.username.data).first()        # 등록된 사용자인지 확인
        if not user:    # db에 없는 사용자인 경우
            error = '존재하지 않는 사용자입니다.'
        elif not check_password_hash(user.password, form.password.data):        # 입력 받은 비밀번호의 해시와 db의 password와 일치하는지 확인
            error = '비밀번호가 올바르지 않습니다.'
        if error is None:       # 사용자도 존재하고 비밀번호도 일치하면
            session.clear()                         # 이미 연결되어있는 세션 클리어
            session['user_id'] = user.id            # 유저 아이디(key)로 세션 생성
            return redirect(url_for('main.index'))  # 메인으로 이동
        flash(error)
    return render_template('auth/login.html', form=form)

@bp.before_app_request      # route 처리 전에 호출되는 함수
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:     # 세션 연결 안됨
        g.user = None       # g = 전역 변수
    else:
        g.user = User.query.get(user_id)

@bp.route('/logout/')
def logout():
    session.clear()     # 세션 클리어 (로그아웃)
    return redirect(url_for('main.index'))
