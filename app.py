# 회원가입을 위한 실행 파일
import os, requests
from flask import Flask, request, redirect, render_template, url_for, session, flash #정보를 제출했을 때 받아오고, 페이지를 이동시키는 함수
from db import db, UserDB   #dp.py의 고객 정보 받아오기
from flask_wtf.csrf import CSRFProtect
from forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash   #비밀번호 관련 함수
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
@app.route('/')
def first():
    return render_template('./first.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = UserDB(
            form.email.data,
            generate_password_hash(form.password.data),  # 비밀번호 해시화
            form.name.data
        )

        # 데이터베이스에 사용자 정보 저장
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('first'))
    return render_template('./register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method=='GET':
        return render_template('./login.html', form=form)
    else:
        email = request.form['email']
        password = request.form['password']
        user = UserDB.query.filter_by(email=email).first()
        if user is not None and check_password_hash(user.password, password):
            session['email'] = user.email
            session['password'] = user.password
            return redirect(url_for('main'))
        else:
            flash('잘못된 로그인을 기입하셨습니다')
            return render_template('./login.html')

@app.route('/main') 
def main():
    if 'email' in session:
        return render_template('./main.html')
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('first'))

if __name__ == '__main__':
    basedir = os.path.abspath(os.path.dirname(__file__))
    dbfile = os.path.join(basedir, 'userInfo.sqlite')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.urandom(24)  # CSRF 공격 방지

    csrf = CSRFProtect()
    csrf.init_app(app)
    db.init_app(app)
    db.app = app

    with app.app_context():
        db.create_all()
    
    app.run(host='127.0.0.1', port=5000, debug=False)    #CSRF 공격 방지