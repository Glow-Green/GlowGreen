from flask import Flask
from flask_socketio import SocketIO


app = Flask(__name__)
socketio = SocketIO()

socketio.init_app(app)

from sollutionChallenge import routes