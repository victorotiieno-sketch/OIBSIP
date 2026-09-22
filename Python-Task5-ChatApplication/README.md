# Chat Application

## OASIS INFOBYTE Python Programming Internship

### Task 5 — Chat Application

A real-time chat application built with Python, Flask, Flask-SocketIO, and SQLite.

## Features

* User registration
* User login and logout
* Password hashing
* Real-time bidirectional messaging
* Multiple chat rooms
* Create and join chat rooms
* SQLite message history
* Message timestamps
* Graceful user disconnect notifications
* Emoji shortcode conversion
* Browser notifications for new messages
* In-app notifications
* Message length validation
* Responsive web interface

## Technologies Used

* Python
* Flask
* Flask-SocketIO
* SQLite
* HTML
* CSS
* JavaScript
* Werkzeug

## Installation

Install the required packages:

bash
python -m pip install flask flask-socketio


## Running the Application

Start the server:

bash
python app.py


Open a browser and visit:

text
http://127.0.0.1:5000


## How to Use

1. Create a user account.
2. Log in with the account.
3. Join the General room or create a new room.
4. Send messages in real time.
5. Open another browser window and log in with another account to test real-time communication.
6. Enable browser notifications when prompted.
7. Use emoji shortcodes such as `:smile:`, `:heart:`, `:thumbsup:`, and `:rocket:`.

## Database Storage

The application automatically creates a SQLite database named `chat.db`.

The database contains:

* `users` — stores usernames and hashed passwords.
* `rooms` — stores available chat rooms.
* `messages` — stores room messages, usernames, and timestamps.

Messages are stored in the SQLite database so that chat history can be loaded when a user joins a room.

## Security Transparency

User passwords are stored as secure password hashes rather than plain text.

Chat messages are stored in the local SQLite database without end-to-end encryption.

The application is intended as an internship project and should not be considered suitable for handling confidential or sensitive communications without additional security controls.

## Project Structure

text
Python-Task5-ChatApplication/
├── app.py
├── chat.db
├── README.md
├── templates/
│   └── index.html
└── static/
    ├── app.js
    └── style.css


## Real-Time Communication

Flask-SocketIO provides real-time communication between connected clients.

Multiple users can connect to the server and exchange messages in the same chat room without refreshing the page.

## Emoji Support

The application converts common emoji shortcodes into Unicode emoji characters.

Examples:

text
:smile: → 😄
:heart: → ❤️
:thumbsup: → 👍
:rocket: → 🚀
:fire: → 🔥


## Notifications

The application provides in-app notifications and can use browser notifications when the chat window is not focused.

## Internship Task

OASIS INFOBYTE Python Programming Internship — Advanced Task 5: Chat Application.
