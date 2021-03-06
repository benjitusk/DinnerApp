# Imports
from jinja2 import select_autoescape, Environment, FileSystemLoader
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
import matplotlib.pyplot as plt
#import pandas as pd
import logging
# import mpld3
import os

class Config(object):
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{}:{}@{}/whatsapp?charset=utf8mb4".format(
        os.getenv("MYSQL_USERNAME"), os.getenv("MYSQL_PASSWORD"), os.getenv("MYSQL_HOSTNAME"))
    SQLALCHEMY_TRACK_MODIFICATIONS = False


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)

# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s@%(funcName)s:%(lineno)d %(levelname)s:\t%(message)s')
# logger = logging
# This is to escape HTML strings in non .html files such as .jinja
app.jinja_env.autoescape = select_autoescape(
    default_for_string=True,
    default=True
)
