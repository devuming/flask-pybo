from datetime import datetime       # 생성일
from flask import Blueprint, render_template, url_for, request
from werkzeug.utils import redirect

from pybo import db
from pybo.models import Question, Answer
from ..forms import AnswerForm

bp = Blueprint('answer', __name__, url_prefix='/answer')

@bp.route('/create/<int:question_id>', methods=('POST', )) # 데이터 처리 : POST 방식
def create(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)

    if form.validate_on_submit():                   # validation check
        content = request.form['content']           # request 값으로 받은 content 내용 받기
        answer = Answer(content=content, create_date=datetime.now())    # Answer 내용으로 객체 생성
        question.answer_set.append(answer)          # question에 연결된 answer db에 추가
        db.session.commit()                         # db 반영
        return redirect(url_for('question.detail', question_id=question_id))  # 상세 페이지로 리다이렉트

    return render_template('question/question_detail.html', question=question, form=form)        # 상세 페이지로 리다이렉트
