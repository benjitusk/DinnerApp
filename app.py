import os
import logging
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template
from jinja2 import select_autoescape, Environment, FileSystemLoader

app = Flask(__name__)
app.config.from_object("config.Config")

# create the logger object
logger = logging.getLogger("app.py") # Name of the logger (so we can tell which logger is currently logging)
logger.setLevel(logging.DEBUG)
# define file handler and set formatter
file_handler = logging.FileHandler(os.cwd() + 'python_server.log')
formatter    = logging.Formatter('[%(asctime)s][%(levelname)s] %(filename)s@%(funcName)s:%(lineno)d:\t%(message)s')
file_handler.setFormatter(formatter)
# add file handler to logger
logger.addHandler(file_handler)

# This is to escape HTML strings in non .html files such as .jinja
app.jinja_env.autoescape = select_autoescape(
    default_for_string=True,
    default=True
)

db = SQLAlchemy(app)



logger.info("Starting server")



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
def makeBold(message):
    # Warning: The output of this function
    # marked as TRUSTED HTML. Make sure
    # we are protected against XSS attacks.
    message=str(message)
    message=message.replace("<", "&lt;")
    message=message.replace(">", "&gt;")
    message=message.replace("&", "&amp;")
    message=message.replace("\"", "&quot;")
    message=message.replace("'", "&#39;")
    message = list(message)
    count = 0
    number_of_asterics = 0
    asteric_index = []
    for char in message:
        if char == "*":
            number_of_asterics += 1
            asteric_index.append(count)
        count += 1
    if number_of_asterics % 2 == 1:
        asteric_index.pop()
    count=0
    for asteric in asteric_index:
        if count % 2==0:
            message[asteric] = "<b>"
        else:
            message[asteric] = "</b>"
        count += 1
    def convert_back_to_string(list_of_chars):
        new = ""
        for x in list_of_chars:
            new += x
        return new
    return convert_back_to_string(message)
app.jinja_env.globals.update(makeBold=makeBold)

@app.route("/")
@app.route("/home")
def home():
    logger.debug("Loading the home page")
    return render_template("home.jinja")


@app.route("/stats")
def stats():
    logger.debug("Loading the stats page")
    return render_template("stats.jinja")


@app.route("/todo/")
def todo():
    logger.debug("Loading the todo page")
    return render_template("todo.jinja")


@app.route("/messages")
def select_chat():
    logger.debug("Loading the messages page")
    result = Chats.query.order_by(Chats.last_at.desc()).all()
    return render_template("select_chat.jinja", chats=result)


@app.route("/messages/chat/<chat_id>")
def messages_by_chat(chat_id):
    logger.debug("Loading the messages_by_chat page")
    chat_messages = Messages.query.order_by(Messages.sent_at.desc()).filter_by(
        chatID=chat_id).all()
    return render_template("display_messages.jinja", messages=chat_messages)


@app.route("/messages/sender/<sender_id>")
def messages_by_sender(sender_id):
    logger.debug("Loading the messages_by_sender page")
    return f"Here would be the messages sent by {sender_id}"


@app.route("/messages/pm/")
def private_messages():
    logger.debug("Loading the private_messages page")
    messages = Messages.query.filter(
        Messages.messageID.like("%@c.us%")).all()
    return render_template("display_messages.jinja", messages=messages)


if __name__ == '__main__':
        app.run(port=1234, debug=True)
