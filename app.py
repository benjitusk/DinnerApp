from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from jinja2 import select_autoescape
import os
app = Flask(__name__)
app.config.from_object("config.Config")

# This is to escape HTML strings in non .html files such as .jinja
app.jinja_env.autoescape = select_autoescape(
    default_for_string=True,
    default=True
)

db = SQLAlchemy(app)


class Messages(db.Model):
    __tablename__ = 'messages'
    ID = db.Column(db.Integer(), primary_key=True, nullable=False)
    sender = db.Column(db.String(100), nullable=False)
    sent_at = db.Column(db.BigInteger(), nullable=False)
    body = db.Column(db.Text(65_536))
    messageID = db.Column(db.String(150))
    type = db.Column(db.String(20), nullable=False)
    has_media = db.Column(db.Boolean(), nullable=False)
    mediaID = db.Column(db.String(150))
    mentionedIds = db.Column(db.Text(65_536))
    chat_name = db.Column(db.String(30))
    pushname = db.Column(db.String(30))
    is_group = db.Column(db.Boolean(), nullable=False)
    chatID = db.Column(db.String(150))
    media_ext = db.Column(db.String(10))

# +--------------+--------------+------+-----+---------+----------------+
# | Field        | Type         | Null | Key | Default | Extra          |
# +--------------+--------------+------+-----+---------+----------------+
# | ID           | int          | NO   | PRI | NULL    | auto_increment |
# | sender       | varchar(100) | NO   |     | NULL    |                |
# | sent_at      | bigint       | NO   |     | NULL    |                |
# | body         | mediumtext   | YES  |     | NULL    |                |
# | messageID    | varchar(150) | YES  |     | NULL    |                |
# | type         | varchar(20)  | NO   |     | NULL    |                |
# | has_media    | tinyint(1)   | NO   |     | NULL    |                |
# | mediaID      | varchar(150) | YES  |     | NULL    |                |
# | mentionedIds | mediumtext   | YES  |     | NULL    |                |
# | chat_name    | varchar(30)  | YES  |     | NULL    |                |
# | pushname     | varchar(30)  | YES  |     | NULL    |                |
# | is_group     | tinyint(1)   | YES  |     | NULL    |                |
# | chatID       | varchar(150) | NO   |     | NULL    |                |
# +--------------+--------------+------+-----+---------+----------------+


class Chats(db.Model):
    __tablename__ = "chats"
    chatID = db.Column(db.String(150), primary_key=True)
    chat_name = db.Column(db.String(30))
    last_at = db.Column(db.BigInteger())
    last_body = db.Column(db.Text(65_536))
    last_sender = db.Column(db.String(100))
    last_type = db.Column(db.String(20))
    lastID = db.Column(db.String(150))
    last_pushname = db.Column(db.String(30))
    is_group = db.Column(db.Boolean())
    contact_display_name = db.Column(db.String(100))
    last_media_ext = db.Column(db.String(10))

# +---------------+--------------+------+-----+---------+-------+
# | Field         | Type         | Null | Key | Default | Extra |
# +---------------+--------------+------+-----+---------+-------+
# | chatID        | varchar(150) | NO   | PRI | NULL    |       |
# | chat_name     | varchar(30)  | NO   |     | NULL    |       |
# | last_at       | bigint       | NO   |     | NULL    |       |
# | last_body     | mediumtext   | YES  |     | NULL    |       |
# | last_sender   | varchar(100) | NO   |     | NULL    |       |
# | last_type     | varchar(20)  | NO   |     | NULL    |       |
# | lastID        | varchar(150) | NO   |     | NULL    |       |
# | last_pushname | varchar(30)  | NO   |     | NULL    |       |
# | is_group      | tinyint(1)   | NO   |     | NULL    |       |
# +---------------+--------------+------+-----+---------+-------+


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.jinja")


@app.route("/stats")
def stats():
    return render_template("stats.jinja")


@app.route("/todo/")
def todo():
    return render_template("todo.jinja")


@app.route("/messages")
def select_chat():
    result = Chats.query.order_by(Chats.last_at.desc()).all()
    return render_template("select_chat.jinja", chats=result)


@app.route("/messages/chat/<chat_id>")
def messages_by_chat(chat_id):
    chat_messages = Messages.query.order_by(Messages.sent_at.desc()).filter_by(
        chatID=chat_id).all()
    return render_template("display_messages.jinja", messages=chat_messages)


@app.route("/messages/sender/<sender_id>")
def messages_by_sender(sender_id):
    return f"Here would be the messages sent by {sender_id}"


@app.route("/messages/pm/")
def private_messages():
    messages = Messages.query.filter(
        Messages.messageID.like("%@c.us%")).all()
    return render_template("display_messages.jinja", messages=messages)


if __name__ == '__main__':
    if os.getenv("PRODUCTION"):
        app.run(port=1234, debug=True, host="0.0.0.0",
                ssl_context=("fullchain.pem", "privkey.pem"))
    else:
        print("Running in dev mode, NOT production")
        app.run(port=1234, debug=True)

