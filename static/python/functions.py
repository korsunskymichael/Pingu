import sqlite3

DATABASE = 'messenger.db'

def get_messages(name: str, variant="all"):
    """
    :param name: user's name type: String
    :param variant: all/latest: all messages for user/latest message for user type: str
                    unread: unread messages by user
    :return: a list of dictionaries. each dictionary is a repr for message
    """
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        message_list = []
        if variant == "unread":
            q = "SELECT message_id, message_sender, message_receiver, message_subject, message, creation_date, read_message FROM messages WHERE message_receiver='%s' AND read_message=0 ORDER BY creation_date" % name
        else:# also covers the latest_message variant
            q = "SELECT message_id, message_sender, message_receiver, message_subject, message, creation_date, read_message FROM messages WHERE message_receiver='%s' ORDER BY creation_date" % name
        try:
            rows = cursor.execute(q)
            message_list = [{'message_id': r[0], 'sender': r[1], 'receiver': r[2], 'subject': r[3], 'message': r[4],
              'creation_date': r[5], 'read_message': r[6]} for r in rows]

        except Exception as e:
            print(e)
        return message_list

def delete_message(id: int):
    """
    :param id: message id requested to be deleted type: int
    :return: row with given id is deleted from messages table, db is updated
    """
    with sqlite3.connect(DATABASE) as connection:
        try:
            cursor = connection.cursor()
            q = "DELETE FROM messages WHERE message_id=%s" % id
            cursor.execute(q)
            connection.commit()
        except Exception as e:
            print(e)

def add_message(message_sender: str, message_receiver: str, message_subject: str, message: str):
    """
    :param message_sender: required type: str
    :param message_receiver: required type: str
    :param message_subject: type: str
    :param message: type: str
    :return: a new row is added to messages table with the specified params
    """
    with sqlite3.connect(DATABASE) as connection:
        try:
            cursor = connection.cursor()
            q = "INSERT INTO messages (message_sender, message_receiver, message_subject, message) VALUES (?, ?, ?, ?)"
            cursor.execute(q, (message_sender, message_receiver, message_subject, message))
            connection.commit()
        except Exception as e:
            print(e)

def add_user(user_name: str, user_password: str):
    """
    :param user_name: type:str
    :param user_password: type:str
    :return: a new row is added to users table with the specified params
    """
    with sqlite3.connect(DATABASE) as connection:
        try:
            cursor = connection.cursor()
            q = "INSERT INTO users (user_name, user_password) VALUES (?, ?)"
            cursor.execute(q, (user_name, user_password))
            connection.commit()
        except Exception as e:
            print(e)

def get_users():
    """
    :return: a ste of users' names is returned
    """
    with sqlite3.connect(DATABASE) as connection:
        try:
            cursor = connection.cursor()
            q = "SELECT user_name FROM users"
            rows = cursor.execute(q)
            return set([r[0] for r in rows])
        except Exception as e:
            print(e)

def check_username(user_name: str, user_password: str):
    """
    :param user_name:
    :param user_password:
    :return: boolean if the username exist in the users table
    """
    with sqlite3.connect(DATABASE) as connection:
        try:
            cursor = connection.cursor()
            q = "SELECT * FROM users WHERE user_name='%s' AND user_password='%s'" % (user_name, user_password)
            rows = cursor.execute(q)
            rowsList = [row for row in rows]
            return (len(rowsList)>0)
        except Exception as e:
            print(e)

def update_read_messages(unread_ids: []):
    """
    :param unread_ids: list of all ids with value 0
    :return: all unread messages status is updated to read (from 0 to 1)
    """
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        q = "UPDATE messages SET read_message=1 WHERE message_id IN (%s)" % unread_ids
        cursor.execute(q)
        connection.commit()
