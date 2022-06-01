from datetime import datetime
from flask import Blueprint, render_template, request, url_for        # render_template : 모델의 데이터를 텍스트로 렌더링 해주는 모듈
from werkzeug.utils import redirect
from .. import db
from pybo.models import Question
from ..forms import QuestionForm, AnswerForm        # pybo 폴더 위치

bp = Blueprint('question', __name__, url_prefix='/question')

@bp.route('/list/')
def _list():
    page = request.args.get('page', type=int, default=1)

    # 데이터 출력
    question_list = Question.query.order_by(Question.create_date.desc())        # 날짜 오름차순으로 데이터리스트 조회
    question_list = question_list.paginate(page, per_page=10)                   # 한 페이지당 게시글 10개씩

    return render_template('question/question_list.html', question_list=question_list)        # question/question_list.html페이지에 question 목록 전달

@bp.route('/detail/<int:question_id>/')  # question_id 변수 받음
def detail(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    return render_template('question/question_detail.html', question=question, form=form)

@bp.route('/create/', methods=('GET', 'POST'))  # question.create
def create():
    form = QuestionForm()

    if request.method == 'POST' and form.validate_on_submit():    # post 형식으로 온 것만 처리, validation 검사 됐는지
        question = Question(subject=form.subject.data, content=form.content.data, create_date=datetime.now())
        db.session.add(question)
        db.session.commit()                         # db 등록
        return redirect(url_for('main.index'))      # 메인으로 이동

    return render_template('question/question_form.html', form=form)