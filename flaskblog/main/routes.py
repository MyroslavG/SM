from flask import render_template, request, Blueprint, url_for, Markup
from flaskblog.models import User, Post, Like#, Comment
from flaskblog import app

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=5)
    return render_template('home.html', posts=posts)

@main.route("/message")
def message():
    return render_template('message.html', title='MESSAGE')

@app.template_filter('mention_links')
def mention_links(comment_text):
    words = comment_text.split()
    new_words = []
    
    for word in words:
        if word.startswith('@'):
            username = word[1:]
            user = User.query.filter_by(username=username).first()
            if user:
                link = f'<a href="{url_for("users.profile", username=user.username)}" style="color: rgb(195, 19, 19);">@{user.username}</a>'
                new_words.append(link)
            else:
                new_words.append(word)
        else:
            new_words.append(word)
    
    return Markup(' '.join(new_words))