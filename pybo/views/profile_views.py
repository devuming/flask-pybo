from flask import Blueprint, url_for, render_template, flash, request, session, g, redirect

from pybo import db
from pybo.models import Question, Answer, Comment, Profile
from pybo.views.auth_views import login_required

bp = Blueprint('profile', __name__, url_prefix='/profile')

@bp.route('/base', methods=('GET',))
@login_required     # 로그인 상태 체크
def base():
    profile = Profile.query.filter(Profile.user_id == g.user.id)
    return render_template('profile/profile_detail.html', menu='base', profile=profile)


@bp.route('/question', methods=('GET',))
@login_required     # 로그인 상태 체크
def question():
    page = request.args.get('page', type=int, default=1)
    question = Question.query.filter(Question.user_id == g.user.id)
    question = question.paginate(page, per_page=10)
    return render_template('profile/profile_detail.html', menu='question', list=question)


@bp.route('/answer', methods=('GET',))
@login_required     # 로그인 상태 체크
def answer():
    page = request.args.get('page', type=int, default=1)
    answer = Answer.query.filter(Answer.user_id == g.user.id)
    answer = answer.paginate(page, per_page=10)

    return render_template('profile/profile_detail.html', menu='answer', list=answer)


@bp.route('/comment', methods=('GET',))
@login_required     # 로그인 상태 체크
def comment():
    page = request.args.get('page', type=int, default=1)
    comment = Comment.query.filter(Comment.user_id == g.user.id)
    comment = comment.paginate(page, per_page=10)

    return render_template('profile/profile_detail.html', menu='comment', list=comment)