# from paths import *
from functions import markUp
from setup import app

app.jinja_env.globals.update(markUp=markUp)

if __name__ == '__main__':
    app.run(port=1234, debug=True)
