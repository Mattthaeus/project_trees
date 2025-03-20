from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class University(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    tuition_fee = db.Column(db.Integer)
    language_requirement = db.Column(db.String(100), nullable=False)
    faculty = db.Column(db.Integer)

    def __repr__(self):
        return f"University <{self.name}>"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(
        db.String(256), nullable=False
    )  # Тут має бути хеш пароля

    def __repr__(self):
        return f"<User {self.username}>"