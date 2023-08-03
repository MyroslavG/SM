from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import User, Post, Like#, Comment
from flaskblog.posts.forms import PostForm
import urllib.parse

posts = Blueprint('posts', __name__)

@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
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