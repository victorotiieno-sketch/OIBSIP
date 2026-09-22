import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("CHAT_SECRET_KEY", "oasis-chat-secret-key")
socketio = SocketIO(app, async_mode="threading")

DATABASE = "chat.db"
sid_rooms = {}


def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_db()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_id INTEGER NOT NULL,
            username TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (room_id) REFERENCES rooms(id)
        )
    """)

    connection.execute(
        "INSERT OR IGNORE INTO rooms (name) VALUES (?)",
        ("General",)
    )

    connection.commit()
    connection.close()


def emoji_convert(text):
    emojis = {
        ":smile:": "😄",
        ":heart:": "❤️",
        ":laughing:": "😂",
        ":thumbsup:": "👍",
        ":sad:": "😢",
        ":fire:": "🔥",
        ":tada:": "🎉",
        ":wink:": "😉",
        ":cry:": "😭",
        ":angry:": "😠",
        ":ok:": "👌",
        ":clap:": "👏",
        ":rocket:": "🚀",
        ":check:": "✅"
    }

    for shortcode, emoji in emojis.items():
        text = text.replace(shortcode, emoji)

    return text


@app.route("/")
def index():
    if "username" in session:
        return redirect(url_for("chat"))

    return render_template("index.html", logged_in=False)


@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    if not username or not password:
        flash("Username and password are required.", "error")
        return redirect(url_for("index"))

    if len(username) < 3:
        flash("Username must contain at least 3 characters.", "error")
        return redirect(url_for("index"))

    if len(password) < 6:
        flash("Password must contain at least 6 characters.", "error")
        return redirect(url_for("index"))

    connection = get_db()

    try:
        connection.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, generate_password_hash(password))
        )
        connection.commit()
    except sqlite3.IntegrityError:
        connection.close()
        flash("Username already exists.", "error")
        return redirect(url_for("index"))

    connection.close()

    session["username"] = username
    return redirect(url_for("chat"))


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    connection = get_db()

    user = connection.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    ).fetchone()

    connection.close()

    if user and check_password_hash(user["password_hash"], password):
        session["username"] = user["username"]
        return redirect(url_for("chat"))

    flash("Invalid username or password.", "error")
    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/chat")
def chat():
    if "username" not in session:
        return redirect(url_for("index"))

    return render_template(
        "index.html",
        logged_in=True,
        username=session["username"]
    )


@app.route("/api/rooms")
def get_rooms():
    if "username" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    connection = get_db()

    rooms = connection.execute(
        "SELECT id, name FROM rooms ORDER BY name"
    ).fetchall()

    connection.close()

    return jsonify([
        {"id": room["id"], "name": room["name"]}
        for room in rooms
    ])


@app.route("/api/rooms", methods=["POST"])
def create_room():
    if "username" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    name = data.get("name", "").strip()

    if not name:
        return jsonify({"error": "Room name is required."}), 400

    if len(name) > 30:
        return jsonify({"error": "Room name is too long."}), 400

    connection = get_db()

    try:
        cursor = connection.execute(
            "INSERT INTO rooms (name) VALUES (?)",
            (name,)
        )
        connection.commit()
        room_id = cursor.lastrowid
    except sqlite3.IntegrityError:
        connection.close()
        return jsonify({"error": "Room already exists."}), 400

    connection.close()

    return jsonify({
        "id": room_id,
        "name": name
    })


@socketio.on("join_room_event")
def handle_join_room(data):
    if "username" not in session:
        return

    room_id = int(data.get("room_id"))

    connection = get_db()

    room = connection.execute(
        "SELECT * FROM rooms WHERE id = ?",
        (room_id,)
    ).fetchone()

    messages = connection.execute(
        """
        SELECT username, message, timestamp
        FROM messages
        WHERE room_id = ?
        ORDER BY id ASC
        LIMIT 100
        """,
        (room_id,)
    ).fetchall()

    connection.close()

    if not room:
        return

    previous_room = sid_rooms.get(request.sid)

    if previous_room:
        leave_room(previous_room)

    join_room(str(room_id))
    sid_rooms[request.sid] = str(room_id)

    history = [
        {
            "username": message["username"],
            "message": message["message"],
            "timestamp": message["timestamp"]
        }
        for message in messages
    ]

    emit(
        "room_history",
        {
            "room_id": room_id,
            "room_name": room["name"],
            "messages": history
        }
    )

    emit(
        "system_message",
        {
            "message": f"{session['username']} joined the room.",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        to=str(room_id)
    )


@socketio.on("send_message")
def handle_message(data):
    if "username" not in session:
        return

    room_id = int(data.get("room_id"))
    message = data.get("message", "").strip()

    if not message:
        return

    if len(message) > 500:
        emit(
            "system_message",
            {
                "message": "Message is too long. Maximum 500 characters.",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        )
        return

    message = emoji_convert(message)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    connection = get_db()

    connection.execute(
        """
        INSERT INTO messages (room_id, username, message, timestamp)
        VALUES (?, ?, ?, ?)
        """,
        (room_id, session["username"], message, timestamp)
    )

    connection.commit()
    connection.close()

    emit(
        "new_message",
        {
            "username": session["username"],
            "message": message,
            "timestamp": timestamp
        },
        to=str(room_id)
    )


@socketio.on("disconnect")
def handle_disconnect():
    room_id = sid_rooms.pop(request.sid, None)

    if room_id:
        username = session.get("username", "A user")

        emit(
            "system_message",
            {
                "message": f"{username} left the room.",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            to=room_id
        )


initialize_database()


if __name__ == "__main__":
    socketio.run(
        app,
        host="127.0.0.1",
        port=5000,
        debug=True,
        allow_unsafe_werkzeug=True
    )