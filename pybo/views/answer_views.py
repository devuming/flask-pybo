from datetime import datetime       # 생성일
from flask import Blueprint, render_template, url_for, request, g
from werkzeug.utils import redirect

from pybo import db
from pybo.models import Question, Answer
from ..forms import AnswerForm
from pybo.views.auth_views import login_required

bp = Blueprint('answer', __name__, url_prefix='/answer')

@bp.route('/create/<int:question_id>', methods=('POST', )) # 데이터 처리 : POST 방식
@login_required     # 로그인 상태 체크
def create(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)

    if form.validate_on_submit():                   # validation check
        content = request.form['content']           # request 값으로 받은 content 내용 받기
        answer = Answer(content=content, create_date=datetime.now(), user=g.user)    # Answer 내용으로 객체 생성
        question.answer_set.append(answer)          # question에 연결된 answer db에 추가
        db.session.commit()                         # db 반영
        return redirect('{}#answer_{}'.format(url_for('question.detail', question_id=question_id), answer.id))  # 상세 페이지로 리다이렉트 > 해당 답변 위치로 스크롤 이동

    return render_template('question/question_detail.html', question=question, form=form)        # 상세 페이지로 리다이렉트

@bp.route('/modify/<int:answer_id>', methods=('GET', 'POST'))
@login_required
def modify(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    if g.user != answer.user:
        flash('수정권한이 없습니다.')
        return redirect(url_for('question.detail', question_id=answer.question_id))
    if request.method == 'POST':
        form = AnswerForm()
        if form.validate_on_submit():
            form.populate_obj(answer)
            answer.modify_date = datetime.now()
            db.session.commit()
            return redirect('{}#answer_{}'.format(url_for('question.detail', question_id=answer.question.id), answer.id))
    else:
        form = AnswerForm(obj=answer)
    return render_template('answer/answer_form.html', answer=answer, form=form)

@bp.route('/delete/<int:answer_id>')
@login_required
def delete(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    question_id = answer.question_id
    if g.user != answer.user:
        flash('삭제권한이 없습니다.')
    else:
        db.session.delete(answer)
        db.session.commit()
    return redirect(url_for('question.detail', question_id=question_id))