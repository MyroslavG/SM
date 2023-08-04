import os
import secrets
from PIL import Image
from flask import url_for
from flask_mail import Message
from flaskblog import app, mail

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images', picture_fn)
    
    output_size = (250, 250)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    
    i.save(picture_path)

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