import sys
activate_this = '/home/dinnerBot/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))
sys.path.insert(0, '/home/dinnerBot')
from app import app as application