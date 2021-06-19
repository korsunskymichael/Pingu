from flask import Flask, redirect, url_for, request, render_template
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, DateTime
from datetime import datetime

app = Flask(__name__)
engine = create_engine('sqlite:///messenger.db', echo=True)
meta = MetaData()

users = Table(
    'users', meta,
    Column('username', String(50), primary_key=True),
    Column('password', String(10))
)

messages = Table(
    'messages', meta,
    Column('message_id', Integer, primary_key=True),
    Column('sender', String(50), ForeignKey('users.username')),
    Column('receiver', String(50), ForeignKey('users.username')),
    Column('subject', String(50)),
    Column('message', String(250)),
    Column("creation_date", DateTime, default=datetime.utcnow())
)

meta.create_all(engine)

#main page
@app.route('/')
def index():
    return render_template("/html/index.html")

#user page
@app.route('/user/<name>')
def user(name):
    return render_template('/html/user.html', name = name)

#login page
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        user = request.form["username"]
        return redirect(url_for("user", name=user))

    return render_template("/html/login.html", error=error)

# sign up page
@app.route("/signup", methods=["GET", "POST"])
def signup():
    error = None

    if request.method == "POST":
        user = request.form.username
        password = request.form.password
        password_again = request.form.password_again
        print(password_again)
        if password == password_again:
            return redirect(url_for('user', name=user))
        else:
            error = "Not identical passwords"
            return redirect(url_for('signup'))
    return render_template('/html/signup.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)

