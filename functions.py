from setup import *


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


class Config(object):
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{}:{}@{}/whatsapp?charset=utf8mb4".format(
        "whatsapp", "secure-whatsapp-bot-password", "whatsfordinnerbinny.com")


def makeBold(message):
    message = str(message)
    message = message.replace("<", "&lt;")
    message = message.replace(">", "&gt;")
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
    count = 0
    for asteric in asteric_index:
        if count % 2 == 0:
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


def loadPlots():
    fig = plt.figure(figsize=(6, 4))
    ages_x = [25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]
    dev_y = [38496, 42000, 46752, 49320, 53200,
             56000, 62136, 64928, 67317, 68748, 73752]
    py_dev_y = [45372, 48876, 53850, 57287, 63016,
                65998, 70003, 70000, 71496, 75370, 83640]
    plt.plot(ages_x, dev_y, color='r', linestyle='--',
             marker='.', label='All Devs')
    plt.plot(ages_x, py_dev_y, color='#444444', marker='o',   label='Python')
    plt.title(
        "A Histogram of Daily Closing Stock Prices for the 5 Largest Banks in the US (5Y Lookback)")
    plt.ylabel("Observations")
    plt.xlabel("Stock Prices")
    plt.tight_layout()
    image_list = []
    picture = mpld3.fig_to_html(fig)
    image_list.append(picture)
    return image_list
