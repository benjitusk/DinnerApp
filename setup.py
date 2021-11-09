# Imports
from jinja2 import select_autoescape, Environment, FileSystemLoader
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import matplotlib.pyplot as plt
import pandas as pd
import logging
import mpld3
import os


app = Flask(__name__)
db = SQLAlchemy(app)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s@%(funcName)s:%(lineno)d %(levelname)s:\t%(message)s')
logger = logging
# This is to escape HTML strings in non .html files such as .jinja
app.jinja_env.autoescape = select_autoescape(
    default_for_string=True,
    default=True
)
