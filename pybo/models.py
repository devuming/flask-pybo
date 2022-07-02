from pybo import db     # pybo.py안의 db 객체 import

question_voter = db.Table(
    'question_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('question_id', db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), primary_key=True)
)   # 다대다 관계 : 하나의 사용자는 여러개의 질문에 추천가능 & 1개의 질문엔 여러 사용자가 추천 가능

answer_voter = db.Table(
    'answer_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('answer_id', db.Integer, db.ForeignKey('answer.id', ondelete='CASCADE'), primary_key=True)
)   # 다대다 관계 : 하나의 사용자는 여러개의 질문에 추천가능 & 1개의 질문엔 여러 사용자가 추천 가능

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('question_set'))      # User에서 Question 역참조 가능
    modify_date = db.Column(db.DateTime(), nullable=True)
    voter = db.relationship('User', secondary=question_voter, backref=db.backref('question_voter_set'))     # secondary > 다대다 연결
    category = db.Column(db.String(200), nullable=False)

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))       # Question모델의 id 필드와 연결, 질문이 삭제되면 answer도 함께 삭제 (CASCADE)
    question = db.relationship('Question', backref=db.backref('answer_set'))       # Question이 Anwser 역참조 가능하도록 연결
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('answer_set'))      # User에서 Answer 역참조 가능
    modify_date = db.Column(db.DateTime(), nullable=True)
    voter = db.relationship('User', secondary=answer_voter, backref=db.backref('answer_voter_set'))     # secondary > 다대다 연결

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    # 프로필 정보
    score = db.Column(db.Integer, nullable=False, server_default='0')       # 파이보 스코어
    introduce = db.Column(db.Text(), nullable=True)                         # 한줄소개
    computer = db.Column(db.String(120), nullable=True)                     # 첫번째 컴퓨터
    editor = db.Column(db.String(120), nullable=True)                       # 좋아하는 에디터
    image = db.Column(db.Text(), nullable=True, default='default.png')      # 프로필 이미지 경로

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('comment_set'))       # User에서 Comment 역참조 가능
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=True)
    modify_date = db.Column(db.DateTime())
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), nullable=True)
    question = db.relationship('Question', backref=db.backref('comment_set'))
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id', ondelete='CASCADE'), nullable=True)
    answer = db.relationship('Answer', backref=db.backref('comment_set'))
