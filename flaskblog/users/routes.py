from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post, Subscription, Comment, Like
from flaskblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm, SearchForm)
from flaskblog.users.utils import save_picture, send_reset_email
from flask_wtf.csrf import generate_csrf

users = Blueprint('users', __name__)

@users.route("/register", methods=['GET', 'POST'])    
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'YOUR ACCOUNT HAS BEEN CREATED! YOU ARE NOW ABLE TO LOG IN', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='REGISTER', form=form)

@users.route("/login", methods=['GET', 'POST'])    
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:    
            flash('LOGIN UNSUCCESSFUL. PLEASE CHECK EMAIL AND PASSWORD', 'danger')
    return render_template('login.html', title='LOGIN', form=form)    

@users.route("/logout")   
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route("/account", methods=['GET', 'POST'])  
@login_required 
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('YOUR ACCOUNT HAS BEEN UPDATED!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='images/' + current_user.image_file)
    return render_template('account.html', title='ACCOUNT', image_file=image_file, form=form) 

@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)           

@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('AN EMAIL HAS BEEN SENT WITH INSTRUCTIONS TO RESET YOUR PASSWORD', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='RESET PASSWORD', form=form)        

@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))  
    user = User.verify_reset_token(token) 
    if user is None:
        flash('THAT IS AN INVALID OR EXPIRED TOKEN', 'warning')     
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'YOUR PASSWORD HAS BEEN UPDATE! YOU ARE NOW ABLE TO LOG IN', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='RESET PASSWORD', form=form)    

@users.route('/profile/<string:username>', methods=['GET', 'POST'])
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5) 

    return render_template('profile.html', user=user, posts=posts)

@users.route('/subscribe/<string:username>', methods=['GET', 'POST'])
@login_required
def subscribe(username):
    user = User.query.filter_by(username=username).first_or_404()
    subscription = Subscription.query.filter_by(subscriber_id=current_user.id, subscribed_to_id=user.id).first()

    if subscription:
        db.session.delete(subscription)
        db.session.commit()
    else:
        new_subscription = Subscription(subscriber_id=current_user.id, subscribed_to_id=user.id)
        db.session.add(new_subscription)
        db.session.commit()

    return redirect(url_for('users.profile', username=username))  
    
@users.route('/message/notification', methods=['GET'])
def notification():
    user = User.query.filter_by(username=current_user.username).first_or_404()

    # Fetch subscribers, comments, and likes specific to the logged-in user
    #logged_in_user_subscribers = user.subscribers.filter_by(subscriber_id=current_user.id).all()
    logged_in_user_comments = Comment.query.filter_by(author=current_user.id).all()
    logged_in_user_likes = Like.query.filter_by(user=current_user).all()

    return render_template('notification.html', user=user,
                           logged_in_user_comments=logged_in_user_comments, logged_in_user_likes=logged_in_user_likes)

@users.route('/message/chat', methods=['GET'])
def chat():
    return render_template('chat.html')                           

@users.context_processor
def base():
    form = SearchForm()
    return dict(form=form)

@users.route('/search', methods=['GET', 'POST'])
def search():           
    form = SearchForm()
    search_results = []

    if request.method == 'POST':
        if form.validate_on_submit():
            searched = form.searched.data
            search_results = User.query.filter(
                User.username.ilike(f'%{searched}%'),
            ).all()
            return render_template('search.html', form=form, search_results=search_results)    
        else:    
            pass
    return render_template('search.html', form=form)