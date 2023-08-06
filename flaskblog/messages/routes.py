from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint, session)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import User, Post, Like#, Message
from flaskblog.posts.forms import PostForm
import urllib.parse
from sqlalchemy import func, desc
from flaskblog.users.utils import post_picture
from flask_socketio import SocketIO, emit

socketio_bp = Blueprint('socketio', __name__, url_prefix='/socketio')

@socketio_bp.route('connect')
def handle_connect():
    # Code to handle new WebSocket connections
    print(f"New client connected: {request.sid}")

@socketio_bp.route('disconnect')
def handle_disconnect():
    # Code to handle WebSocket disconnections
    print(f"Client disconnected: {request.sid}")

@socketio_bp.route('message')
def handle_message(data):
    # Code to handle incoming messages
    sender_id = data.get('sender_id')
    receiver_id = data.get('receiver_id')
    message_content = data.get('message_content')

    # Save the message to the database (use your Message model for this)
    new_message = Message(sender_id=sender_id, receiver_id=receiver_id, message_content=message_content)
    db.session.add(new_message)
    db.session.commit()

    # Broadcast the message to the recipient's WebSocket connection
    socketio.emit('message', data, room=f"user_{receiver_id}")

    # Send an acknowledgement to the sender
    socketio.emit('message_ack', {'status': 'Message sent successfully'}, room=request.sid)
