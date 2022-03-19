from flask import Flask, render_template, current_app
from flask_socketio import SocketIO, send, join_room, leave_room
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
socket = SocketIO(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

room = ""

class History(db.Model):
    __tablename__ = "history"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(20), nullable=False)
    room = db.Column(db.String(20), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    
    def __repr__(self):
        return f"Message(id={self.id}, message={self.message}, room={self.room}, date={self.date})"

db.create_all()

@socket.on("message")
def handle_message(data):
    room = data["room"]
    message = data["msg"]
    username = data["username"]
    history = History(message=message, room=room, username=username)
    db.session.add(history)
    db.session.commit()
    send(username + ": " + message, to=room, broadcast=True)

@socket.on("join")
def join(data):
    global room
    username = data["username"]
    room = data["room"]
    print("Room: " + room)
    print(username, room)
    join_room(room)
    send(username + " has joined the room {}.".format(room), room=room)

@socket.on("leave")
def leave(data):
    username = data["username"]
    room = data["room"]
    leave_room(room)
    send(username + " has left the room {}.".format(room), room=room)

@app.route("/")
def index():
    history = History.query.all()
    print(room)
    return render_template("index.html", history=history, room=room)

if __name__ == "__main__":
    socket.run(app, debug=True)