from flask import Blueprint, url_for, render_template, flash, request, session, g, redirect

from pybo import db
from pybo.models import Question, Answer, Comment, User
from pybo.views.auth_views import login_required

bp = Blueprint('profile', __name__, url_prefix='/profile')

@bp.route('/base', methods=('GET',))
@login_required     # 로그인 상태 체크
def base():
    user = User.query.filter_by(id=g.user.id).first()
    return render_template('profile/profile_detail.html', menu='base', user=user)


@bp.route('/question', methods=('GET',))
@login_required     # 로그인 상태 체크
def question():
    page = request.args.get('page', type=int, default=1)
    question_list = Question.query.filter(Question.user_id == g.user.id)
    question_list = question_list.paginate(page, per_page=10)
    return render_template('profile/profile_detail.html', menu='question', list=question_list)


@bp.route('/answer', methods=('GET',))
@login_required     # 로그인 상태 체크
def answer():
    page = request.args.get('page', type=int, default=1)
    answer_list = Answer.query.filter(Answer.user_id == g.user.id)
    answer_list = answer_list.paginate(page, per_page=10)

    return render_template('profile/profile_detail.html', menu='answer', list=answer_list)


@bp.route('/comment', methods=('GET',))
@login_required     # 로그인 상태 체크
def comment():
    page = request.args.get('page', type=int, default=1)
    comment_list = Comment.query.filter(Comment.user_id == g.user.id)
    comment_list = comment_list.paginate(page, per_page=10)

    return render_template('profile/profile_detail.html', menu='comment', list=comment_list)