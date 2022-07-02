from flask import Blueprint, render_template, g, request, url_for
from werkzeug.utils import redirect
from werkzeug.security import generate_password_hash, check_password_hash  # 비밀번호 암호화 생성

from pybo import db
from pybo.models import Profile, User
from pybo.forms import ProfileForm, PasswordChangeForm
from pybo.views.auth_views import login_required

bp = Blueprint('settings', __name__, url_prefix='/settings')


@bp.route('/base', methods=('GET','POST'))
@login_required     # 로그인 상태 체크
def base():
    profile = Profile.query.filter_by(user_id=g.user.id).first()
    form = ProfileForm()

    if request.method == 'POST' and form.validate_on_submit():    # post 형식으로 온 것만 처리, validation 검사 됐는지
        profile = Profile.query.filter_by(user_id=g.user.id).first()

        if not profile: # 등록된 프로필이 없으면
            # 신규 등록
            profile = Profile(user_id=g.user.id, introduce=form.introduce.data, computer=form.computer.data, editor=form.editor.data)
            db.session.add(profile)
            db.session.commit()
        else:
            # 수정
            form.populate_obj(profile)
            db.session.commit()

    return render_template('profile/settings_base.html', menu='base', form=form, profile=profile)

@bp.route('/image', methods=('GET', 'POST'))
@login_required     # 로그인 상태 체크
def image():
    profile = Profile.query.filter(Profile.user_id == g.user.id)
    form = ProfileForm()
    return render_template('profile/settings_image.html', menu='image', form=form, profile=profile)

@bp.route('/password', methods=('GET', 'POST'))
@login_required     # 로그인 상태 체크
def password():
    profile = Profile.query.filter(Profile.user_id == g.user.id)
    form = PasswordChangeForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()    # username의 데이터 가져오기
        if not user :    # db에 같은 username으로 이미 등록된 user인지 확인
            error = '존재하지 않는 사용자입니다.'
        elif not check_password_hash(user.password, form.password.data):  # 입력 받은 비밀번호의 해시와 db의 password와 일치하는지 확인
            error = '비밀번호가 올바르지 않습니다.'
        else:   # 비밀번호 수정
            user = User(username=form.username.data,
                        password=generate_password_hash(form.password1.data),
                        email=form.email.data)
            db.session.add(user)
            db.session.commit()

    return render_template('profile/settings_password.html', menu='password', form=form, profile=profile)


@bp.route('/email', methods=('GET', 'POST'))
@login_required     # 로그인 상태 체크
def email():
    profile = Profile.query.filter(Profile.user_id == g.user.id)
    form = ProfileForm()
    return render_template('profile/settings_email.html', menu='email', form=form, profile=profile)