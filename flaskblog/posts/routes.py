from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint, session)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import User, Post, Like, Comment
from flaskblog.posts.forms import PostForm, CommentForm
import urllib.parse
from sqlalchemy import func, desc
from flaskblog.users.utils import post_picture

posts = Blueprint('posts', __name__)

@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        picture_file = None
        video_file = None
        if form.media.data:
            video_url = form.media.data
        #if form.picture.data:

        post = Post(title=form.title.data, content=form.content.data, author=current_user, video_file=video_url)
        db.session.add(post)
        db.session.commit()
        flash('YOUR POST HAS BEEN CREATED!', 'success')
        return redirect(url_for('main.home'))      
    return render_template('create_post.html', title = 'NEW POST', form=form, legend='NEW POST')

@posts.route("/post/<int:post_id>", methods=['GET', 'POST'])  
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post, legend='NEW POST')

@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])  
@login_required
def update_post(post_id):    
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('YOUR POST HAS BEEN UPDATED!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='UPDATE POST', form=form, legend='UPDATE POST')  

@posts.route("/post/<int:post_id>/delete", methods=['POST'])  
@login_required
def delete_post(post_id):      
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    likes_to_delete = db.session.query(Like).filter(Like.post_id == post_id).all()
    for item in likes_to_delete:
        db.session.delete(item)
    db.session.delete(post)
    db.session.commit()
    flash('YOUR POST HAS BEEN DELETED!', 'success')
    return redirect(url_for('main.home'))

@posts.route('/like_post/<int:post_id>', methods=['GET'])
@login_required
def like_post(post_id):
    post = Post.query.filter_by(id=post_id)
    like = Like.query.filter_by(
        author=current_user.id, post_id=post_id).first()
    if not post:
        flash('POST DOES NOT EXIST', 'danger')
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(author=current_user.id, post_id=post_id)    
        db.session.add(like)
        db.session.commit()
    return redirect(url_for('main.home'))    

@posts.route('/profile_like_post/<string:username>/<int:post_id>', methods=['GET'])
@login_required
def profile_like_post(username, post_id):
    decoded_username = urllib.parse.unquote(username)
    user = User.query.filter_by(username=decoded_username).first()
    post = Post.query.filter_by(id=post_id, user_id=user.id)
    like = Like.query.filter_by(
        author=current_user.id, post_id=post_id).first()
    if not post:
        flash('POST DOES NOT EXIST', 'danger')
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(author=current_user.id, post_id=post_id)    
        db.session.add(like)
        db.session.commit()
    return redirect(url_for('users.profile', username=username))    

@posts.route('/comment_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def comment_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        flash('POST DOES NOT EXIST', 'danger')
    else:
        form = CommentForm()
        if form.validate_on_submit():
            text = form.comment_text.data
            new_comment = Comment(text=text, author=current_user.id, post_id=post_id)
            db.session.add(new_comment)
            db.session.commit()
            flash('COMMENT ADDED', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('PLEASE ENTER A COMMENT', 'danger')

    return render_template('comment.html', title='LOGIN', form=form, post=post) 

@posts.route('/trending')
def trending():
    most_liked_posts = db.session.query(
        Post, func.count(Like.id).label('like_count')
    ).outerjoin(Like).group_by(Post).order_by(desc('like_count')).all()

    return render_template('trending.html', posts=most_liked_posts)    