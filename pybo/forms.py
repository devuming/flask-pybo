from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, EmailField, SelectField  # 데이터 검증을 위한 모듈
from wtforms.validators import DataRequired, Length, EqualTo, Email         # 빈 데이터 인지 검증


class QuestionForm(FlaskForm):
    subject = StringField('제목', validators=[DataRequired('제목은 필수 입력 항목입니다.')])    # 필수 입력 TextBox : 입력 안했을시 경고
    category = SelectField('카테고리', choices=['qna', 'lesson', 'free'])
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수 입력 항목입니다.')])

class AnswerForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수 입력 항목입니다.')])

class UserCreateForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    password1 = PasswordField('비밀번호', validators=[DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다.')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired()])
    email = EmailField('이메일', validators=[DataRequired(), Email()])

class UserLoginForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('비밀번호', validators=[DataRequired()])

class CommentForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired()])

class ProfileForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    introduce = TextAreaField('한줄소개')
    computer = TextAreaField('나의 첫번째 컴퓨터', validators=[Length(max=120)])
    editor = TextAreaField('좋아하는 에디터', validators=[Length(max=120)])

class PasswordChangeForm(FlaskForm):
    password = PasswordField('기존 비밀번호', validators=[DataRequired()])
    password_new = PasswordField('새 비밀번호', validators=[DataRequired(), EqualTo('password_new2', '비밀번호가 일치하지 않습니다.')])
    password_new2 = PasswordField('새 비밀번호 확인', validators=[DataRequired()])