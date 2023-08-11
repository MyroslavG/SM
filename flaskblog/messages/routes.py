from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint, session)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import User, Post, Like, Message, Chat
from flaskblog.posts.forms import PostForm
from sqlalchemy import func, desc
from flaskblog.users.utils import post_picture
import os
from werkzeug.utils import secure_filename  
import boto3
from datetime import datetime
#from flask_socketio import SocketIO, emit, join_room
#from flaskblog import socketio

chats = Blueprint('chats', __name__, url_prefix='/chat')

@chats.route('/all_chats')
def all_chats():
    other_users = User.query.filter(User.id != current_user.id).all()
    return render_template('all_chats.html', all_recipients=other_users)

@chats.route('/create/<int:recipient_id>')
def chat_with_user(recipient_id):
    chat = Chat.query.filter(
        Chat.participants.any(id=current_user.id),
        Chat.participants.any(id=recipient_id)
    ).first()

    if chat is None:
        new_chat = Chat()
        new_chat.participants.append(current_user)
        new_chat.participants.append(User.query.get(recipient_id))
        db.session.add(new_chat)
        db.session.commit()
        chat = new_chat

    if request.method == 'POST':
        message_content = request.form.get('message_content')
        new_message = Message(sender=current_user, recipient=User.query.get(recipient_id), chat=chat, message_content=message_content)
        db.session.add(new_message)
        db.session.commit()

    messages = Message.query.filter_by(chat=chat).order_by(Message.timestamp.asc()).all()

    return render_template('chat.html', chat=chat, messages=messages)

@chats.route('/<int:chat_id>/send', methods=['POST'])
def send_message(chat_id):
    message_content = request.form.get('message_content')
    
    chat = Chat.query.get_or_404(chat_id)

    recipient = chat.participants[0] if current_user.id == chat.participants[1].id else chat.participants[1]

    new_message = Message(sender=current_user, recipient=recipient, chat=chat, message_content=message_content, timestamp=datetime.utcnow())
    db.session.add(new_message)
    db.session.commit()

    return redirect(url_for('chats.chat_with_user', chat_id=chat_id, recipient_id=recipient.id))
