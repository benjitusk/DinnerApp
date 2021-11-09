from setup import *
from functions import *


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.jinja")


@app.route("/stats")
def stats():
    pictures = loadPlots()
    return render_template("stats.jinja", pictures=pictures)


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

@app.route("/beta/chats")
def beta_chats():
    logger.debug("Loading the beta_chats page")
    chats = Chats.query.order_by(Chats.last_at.desc()).all()
    return render_template("beta_chats.jinja", chats=chats, messages=[])

@app.route("/beta/chats/<chat_id>")
def beta_messages_by_chat(chat_id):
    logger.debug("Loading the beta_messages_by_chat page")
    chats = Chats.query.order_by(Chats.last_at.desc()).all()
    chat_messages = Messages.query.order_by(Messages.sent_at.desc()).filter_by(
        chatID=chat_id).all()
    return render_template("beta_chats.jinja", messages=chat_messages, chats=chats)

@app.route("/beta/chats/<chat_id>.json")
def beta_chats_json(chat_id):
    logger.debug("Loading the beta_chats_json page")
    chat_messages = Messages.query.order_by(Messages.sent_at.desc()).filter_by(
        chatID=chat_id).all()
    return jsonify([message.toDict() for message in chat_messages])
