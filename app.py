from paths import *
from functions import *

app.jinja_env.globals.update(markUp=markUp)
app.config.from_object(Config)

if __name__ == '__main__':
    app.run(port=1234, debug=True)
# test message
