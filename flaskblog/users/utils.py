import os
import secrets
from PIL import Image
from flask import url_for
from flask_mail import Message
from flaskblog import app, mail
from flaskblog.s3_utils import upload_to_s3, allowed_file
from flaskblog.models import User, Message

def user_has_unread_message(current_user_id, recipient_id):
    user = User.query.get(current_user_id)
    unread_messages = Message.query.filter_by(recipient=user, sender_id=recipient_id, is_read=False).count()
    return unread_messages > 0

import requests
import io

def resize_image(uploaded_file, filename):
    image = Image.open(uploaded_file)

    width_percent = 1000 / image.width
    height_percent = 1000 / image.height
    resize_percent = min(width_percent, height_percent)
    new_width = int(image.width * resize_percent)
    new_height = int(image.height * resize_percent)
    
    image = image.resize((new_width, new_height))
    return image, filename

def save_picture(form_picture, filename):
    # random_hex = secrets.token_hex(8)
    # _, f_ext = os.path.splitext(form_picture.filename)
    # picture_fn = random_hex + f_ext
    # picture_path = os.path.join(app.root_path, 'static/images', picture_fn)    
    # output_size = (250, 250)
    # i = Image.open(form_picture)
    # i.thumbnail(output_size)    
    # i.save(picture_path)

    picture_fn = upload_to_s3(form_picture)
    return picture_fn

def post_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    #picture_path = os.path.join(app.root_path, 'static/images', picture_fn)
    
    output_size = (1024, 1024)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    
    i.save(picture_path)

    return picture_fn
    

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('PASSWORD RESET REQUEST', 
            sender='noreply@demo.com', 
            recipients=[user.email])
    msg.body = f'''TO RESET YOUR PASSWORD, VISIT THE FOLLOWING LINK:
{url_for('users.reset_token', token=token, _external=True)}    
    
IF YOU DID NOT MAKE THIS REQUEST THEN SIMPLY IGNORE THIS EMAIL AND NO CHANGES WILL BE MADE.    
'''        
    mail.send(msg)    