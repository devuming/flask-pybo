from datetime import datetime
from flask import Blueprint, render_template, request, url_for, g, flash       # render_template : 모델의 데이터를 텍스트로 렌더링 해주는 모듈
from werkzeug.utils import redirect
from sqlalchemy import func

from .. import db
from pybo.models import Question, Answer, User, question_voter, answer_voter
from ..forms import QuestionForm, AnswerForm        # pybo 폴더 위치
from pybo.views.auth_views import login_required

bp = Blueprint('question', __name__, url_prefix='/question')

@bp.route('/list/')
def _list():
    # 입력 파라미터
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')               # 검색 키워드
    so = request.args.get('so', type=str, default='recent')         # 정렬 기준
    category = request.args.get('category', type=str, default='total')    # 카테고리 기준

    # 정렬
    if so == 'recommend':
        sub_query = db.session.query(question_voter.c.question_id, func.count('*').label('num_voter')).group_by(question_voter.c.question_id).subquery()        # 추천 수
        question_list = Question.query.outerjoin(sub_query, Question.id == sub_query.c.question_id).order_by(sub_query.c.num_voter.desc(), Question.create_date.desc())
    elif so == 'popular':
        sub_query = db.session.query(Answer.question_id, func.count('*').label('num_answer')).group_by(Answer.question_id).subquery()   # 답변 수 
        question_list = Question.query.outerjoin(sub_query, Question.id == sub_query.c.question_id).order_by(sub_query.c.num_answer.desc(), Question.create_date.desc())
    else:       # 최근 질문
        question_list = Question.query.order_by(Question.create_date.desc())
    
    # 검색
    if kw:
        search = '%%{}%%'.format(kw)
        sub_query = db.session.query(Answer.question_id, Answer.content, User.username)\
                              .join(User, Answer.user_id == User.id).subquery()             # userid로 Answer과 User 조인
        question_list = question_list.join(User)\
                        .outerjoin(sub_query, sub_query.c.question_id == Question.id)\
                        .filter(Question.subject.ilike(search) |    # 질문제목
                                Question.content.ilike(search) |    # 질문내용
                                User.username.ilike(search) |       # 질문작성자
                                sub_query.c.content.ilike(search) | # 답변내용
                                sub_query.c.username.ilike(search)  # 답변작성자
                                 )\
                        .distinct()

    if category != '' and category != 'total':     # 카테고리
        question_list = question_list.filter(Question.category == category)
        question_list = question_list.filter(Question.category == category)

    # 페이징
    question_list = question_list.paginate(page, per_page=10)                   # 한 페이지당 게시글 10개씩
    return render_template('question/question_list.html', question_list=question_list, page=page, kw=kw, so=so, category=category)  # question/question_list.html페이지에 question 목록 전달

@bp.route('/detail/<int:question_id>/')  # question_id 변수 받음
def detail(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)

    # 답변 추천순 정렬
    sub_query = db.session.query(answer_voter.c.answer_id, func.count('*').label('num_voter'))\
                          .group_by(answer_voter.c.answer_id).subquery()  # 답변 추천 수

    answer_set = Answer.query.outerjoin(sub_query, Answer.id == sub_query.c.answer_id).order_by(sub_query.c.num_voter.desc(), Answer.create_date.desc())
    answer_set.join(User).outerjoin(sub_query, sub_query.c.answer_id == Answer.id).distinct()

    return render_template('question/question_detail.html', question=question, answer_set=answer_set, form=form)

@bp.route('/create/', methods=('GET', 'POST'))  # question.create
@login_required
def create():
    form = QuestionForm()

    if request.method == 'POST' and form.validate_on_submit():    # post 형식으로 온 것만 처리, validation 검사 됐는지
        question = Question(subject=form.subject.data, content=form.content.data, create_date=datetime.now(), user=g.user, category=form.category.data)
        db.session.add(question)
        db.session.commit()                         # db 등록
        return redirect(url_for('main.index'))      # 메인으로 이동

    return render_template('question/question_form.html', form=form)

@bp.route('/modify/<int:question_id>', methods=('GET', 'POST'))
@login_required
def modify(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('수정권한이 없습니다.')
        return redirect(url_for('question.detail', question_id=question_id))
    if request.method == 'POST':
        form = QuestionForm()
        if form.validate_on_submit():
            form.populate_obj(question)
            question.modify_date = datetime.now()   # 수정일시
            db.session.commit()
            return redirect(url_for('question.detail', question_id=question_id))
    else:
        form = QuestionForm(obj=question)
    return render_template('question/question_form.html', form=form)

@bp.route('/delete/<int:question_id>')
@login_required
def delete(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('삭제권한이 없습니다.')
        return redirect(url_for('question.detail', question_id=question_id))

    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('question._list'))
