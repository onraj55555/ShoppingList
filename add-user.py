#!python
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config.from_pyfile("config.py", silent=True)

db = SQLAlchemy(app)

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)

with app.app_context():
    db.create_all()

    username = input("Enter username: ")
    password = input("Enter password: ")

    if Users.query.filter_by(username=username).first():
        print("User already exists!")
        exit(1)

    hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

    new_user = Users(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    print("New user added!")
