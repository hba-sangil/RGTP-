from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# email을 primary key로 설정한 UserDB 모델
class UserDB(db.Model):
    __tablename__ = 'userInfo'
    email = db.Column(db.String(100), primary_key=True)
    password = db.Column(db.String(100))
    username = db.Column(db.String(10))

    def __init__(self, email, password, username):
        self.email = email
        self.password = password
        self.username = username