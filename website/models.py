from flask_sqlalchemy import SQLAlchemy
# from website.database import Base

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(120))
    current_exercise = db.Column(db.Integer, db.ForeignKey("exercise.id"), nullable=False)

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password
        self.current_exercise = 0

    def __repr__(self):
        return '<User %r>' % self.username


class Exercise (db.Model):
    __tablename__ = "exercise"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, unique=True, nullable=False)
    test_code = db.Column(db.String, unique=True, nullable=False)
    check_code = db.Column(db.String, unique=True, nullable=False)

    def __init__(self, description, test_code, check_code):
        self.description = description
        self.test_code = test_code
        self.check_code = check_code

    def __repr__(self):
        return '<Client %r>' % self.name