from flask import render_template, request, Blueprint
from flaskblog.models import Post, Like#, Comment

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