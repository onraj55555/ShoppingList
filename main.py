#!python
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from werkzeug.security import check_password_hash
# from flask_socketio import SocketIO, send, emit, join_room, leave_room

app = Flask(__name__)
app.config.from_pyfile("config.py", silent=True)

# socketio = SocketIO(app)

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)

data_file_name = "data"
room = "global"

def read_from_file():
    with open(data_file_name, 'r') as f:
        return f.read().split()

data = read_from_file()
session_ids = set()

def save_to_file():
    with open(data_file_name, 'w') as f:
        f.write(" ".join(data))


def add_article(article):
    if data.count(article) == 0:
        data.append(article)
        save_to_file()

def remove_article(articles):
    for article in articles:
        if data.count(article) != 0:
            data.remove(article)
        save_to_file()

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# @socketio.on('join')
# @login_required
# def handle_join():
#     session_ids.add(request.sid)
#     join_room(room, sid=request.sid)
#     emit('message', data, broadcast=False) # Only notify the new client with the data
#
# @socketio.on('message')
# @login_required
# def handle_message(msg):
#     emit('message', data, broadcast=False)
#
# @socketio.on('disconnect')
# @login_required
# def handle_disconnect():
#     session_ids.remove(request.sid)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username").strip().lower()
        password = request.form.get("password")

        user = Users.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("shopping"))
        else:
            return render_template("login.html")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/shopping", methods = ["GET", "POST"])
@app.route("/shopping/<action>", methods = ["GET", "POST"])
@login_required
def shopping(action = None):
    if request.method == "POST":
        if action == "add":
            article = request.form["article"]
            if article != "":
                add_article(article)
        if action == "remove":
            articles_to_remove = []
            for d in data:
                t = request.form.get(d)
                if t != None:
                    articles_to_remove.append(d)
            remove_article(articles_to_remove)
        return redirect(url_for("shopping"))

    return render_template("shopping-list.html")

@app.route("/api/data")
@login_required
def api_data():
    return data

@app.route("/")
def home():
    return redirect(url_for("login"))

if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
    #app.run(host="0.0.0.0", port=8080, debug=True)
