from flask import Flask
from werkzeug.contrib.fixers import ProxyFix
from chessrest import api

app = Flask(__name__)

if __name__ == "__main__":

    app.wsgi_app = ProxyFix(app.wsgi_app)
    api.init_app(app)
    app.run(debug=True)

