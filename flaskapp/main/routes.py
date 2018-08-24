from flask import Blueprint, request, render_template
from flaskapp.models import Posts
from flask_login import login_required

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    posts = Posts.query.order_by(Posts.pub_date.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@main.route('/about')
def about():
    return render_template('about.html')


@main.route('/contact')
def contact():
    return render_template('about.html')


@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')