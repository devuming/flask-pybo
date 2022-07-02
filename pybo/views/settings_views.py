from flask import Blueprint, render_template, g, request, url_for, flash
from werkzeug.utils import redirect
from werkzeug.security import generate_password_hash, check_password_hash  # 비밀번호 암호화 생성

from pybo import db
from pybo.models import User
from pybo.forms import ProfileForm, PasswordChangeForm
from pybo.views.auth_views import login_required

bp = Blueprint('settings', __name__, url_prefix='/settings')


@bp.route('/base', methods=('GET','POST'))
@login_required     # 로그인 상태 체크
def base():
    user = User.query.filter_by(id=g.user.id).first()
    form = ProfileForm()

    if request.method == 'POST' and form.validate_on_submit():    # post 형식으로 온 것만 처리, validation 검사 됐는지
        error = ''
        if not user:    # 등록된 프로필이 없으면
            # 오류 발생
            error = "존재하지 않는 사용자입니다."
        elif g.user.username != form.username.data:     # username 변경 시,
            user_name = User.query.filter_by(username=form.username.data).first()

            if user_name:                           # 동일한 username 있는 경우
                user.username = form.username.data
                error = "이미 등록된 아이디 입니다."

        if error != '':     # 에러 있는 경우 출력
            flash(error)
            return render_template('profile/settings_base.html', menu='base', form=form, user=user)
        # 수정
        user.username = form.username.data
        user.introduce = form.introduce.data
        user.computer = form.computer.data
        user.editor = form.editor.data
        db.session.commit()
        return redirect(url_for('settings.base'))

    return render_template('profile/settings_base.html', menu='base', form=form, user=user)

@bp.route('/image', methods=('GET', 'POST'))
@login_required     # 로그인 상태 체크
def image():
    user = User.query.filter_by(id=g.user.id).first()
    form = ProfileForm()
    return render_template('profile/settings_image.html', menu='image', form=form, user=user)

@bp.route('/password', methods=('GET', 'POST'))
@login_required     # 로그인 상태 체크
def password():
    user = User.query.filter_by(id=g.user.id).first()
    form = PasswordChangeForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = ''
        if not user:    # db에 같은 username으로 이미 등록된 user인지 확인
            error = '존재하지 않는 사용자입니다.'
        elif not check_password_hash(user.password, form.password.data):  # 입력 받은 비밀번호의 해시와 db의 password와 일치하는지 확인
            error = '비밀번호가 올바르지 않습니다.'
        else:   # 비밀번호 수정
            user.password = generate_password_hash(form.password_new.data)
            db.session.commit()
            flash('비밀번호가 변경되었습니다', 'info')

            return redirect(url_for('settings.password'))

        flash(error)
    return render_template('profile/settings_password.html', menu='password', form=form, user=user)


@bp.route('/email', methods=('GET', 'POST'))
@login_required     # 로그인 상태 체크
def email():
    user = User.query.filter_by(id=g.user.id).first()
    form = ProfileForm()
    return render_template('profile/settings_email.html', menu='email', form=form, user=user)