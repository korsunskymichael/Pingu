from flask import Flask, redirect, url_for, request, render_template
from static.python.functions import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("/html/index.html")

@app.route('/login', methods = ["POST", "GET"])
def login():
    if  request.method == "POST":
        user_name = request.form["username"]
        user_password = request.form["password"]
        valid_user = check_username(user_name, user_password)
        if valid_user:
            return redirect(url_for("user", name = user_name))
        else:
            print("incorrect user or password")
            return redirect(url_for("login"))
    return render_template("/html/login.html")

@app.route('/signup', methods = ["POST", "GET"])
def signup():
    if request.method == "POST":
        user_name = request.form['username']
        user_password = request.form["password"]
        usernames = get_users()

        if user_name not in usernames:
            add_user(user_name, user_password)
            return redirect(url_for("login"))
        else:
            print("user name already exist")
            return redirect(url_for("signup"))

    return render_template('/html/signup.html')

@app.route('/user/<name>', methods = ["POST", "GET"])
def user(name):
    usernames = get_users()
    return render_template('/html/user.html', name=name, usernames=usernames)

@app.route("/write_message/<name>", methods = ["POST", "GET"])
def write_message(name):
    message_sender = name
    message_receiver = request.form["receiver"]
    message_subject = request.form["subject"]
    message = request.form["message"]
    add_message(message_sender, message_receiver, message_subject, message)
    return redirect(url_for("user", name = name))


@app.route('/delete_by_id/<name>', methods = ["POST", "GET"])
def delete_by_id(name):
    message_id = request.form["message_id"]
    delete_message(message_id)
    return redirect(url_for("user", name=name))

@app.route('/all_messages/<name>', methods = ["POST", "GET"])
def show_all_messages(name):
    all_messages = get_messages(name)
    unread_ids = [message.get("message_id") for message in all_messages if int(message.get("read_message")) == 0]
    print(len(unread_ids))
    if len(unread_ids) >0:
        update_read_messages(tuple(unread_ids))
    return render_template('/html/messages.html', name=name, messages=all_messages)


@app.route('/unread_messages/<name>', methods = ["POST", "GET"])
def show_unread_messages(name):
    unread_messages = get_messages(name)
    unread_ids = [message.get("message_id") for message in unread_messages if int(message.get("read_message")) == 0]
    if len(unread_ids) > 0:
        update_read_messages(tuple(unread_ids))
    return render_template('/html/messages.html', name=name, messages=unread_messages)

@app.route('/latest_message/<name>', methods = ["POST", "GET"])
def show_latest_message(name):
    latest_message =[]
    messages = get_messages(name, "latest")
    if len(messages) > 0:
        latest_message = [messages[0]]
        update_read_messages(tuple([latest_message[0].get("message_id")]))
    return render_template('/html/messages.html', name=name, messages=latest_message)


if __name__ == '__main__':
    connection = sqlite3.connect(DATABASE)

    path = 'static/sql/messages_init.sql'
    q = open(path, 'r').read()
    cursor = connection.cursor()
    cursor.execute(q)

    path = 'static/sql/users_init.sql'
    q = open(path, 'r').read()
    cursor = connection.cursor()
    cursor.execute(q)

    path = 'static/sql/insert_messages.sql'
    q = open(path, 'r').read()
    cursor = connection.cursor()
    cursor.execute(q)

    path = 'static/sql/insert_users.sql'
    q = open(path, 'r').read()
    cursor = connection.cursor()
    cursor.execute(q)

    connection.commit()
    connection.close()

    app.run(debug=True)

