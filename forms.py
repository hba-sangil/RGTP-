# 사용자로부터 입력받은 정보를 관리하는 파일
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo    # 비밀번호 유효성 검사

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    confirm_password = PasswordField('confirm_password', validators=[DataRequired(), EqualTo('password')])
    name = StringField('name', validators=[DataRequired()])

class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])