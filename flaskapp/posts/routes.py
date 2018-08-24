from flask import Blueprint, flash, request, render_template, redirect, url_for, abort
from .forms import ArticleForm
from flask_login import current_user, login_required
from flaskapp.models import Posts, User
from flaskapp import db

posts = Blueprint('posts', __name__)


@posts.route('/add_posts', methods=['POST', 'GET'])
@login_required
def add_posts():
    form = ArticleForm()
    if request.method == 'POST' and form.validate_on_submit():
        title = form.title.data
        author = form.author.data
        body = form.body.data
        posts= Posts(title=title, author=author, body=body)
        db.session.add(posts)
        db.session.commit()
        flash('You have successfully post your article', 'success')
        return redirect(url_for('posts.add_posts'))
    return render_template('add_posts.html', form=form)


@posts.route('/show_posts')
@login_required
def show_posts():
    page = request.args.get('page', 1, type=int)
    posts = Posts.query.all()
    page_paginates = Posts.query.paginate(page=page, per_page=5)
    return render_template('show_posts.html', posts=posts, page_paginates=page_paginates)


@posts.route('/user/edit_post/<int:id>', methods=['POST', 'GET'])
@login_required
def edit_post(id):
    posts = Posts.query.get(id)
    form = ArticleForm()
    if form.validate_on_submit():
        posts.title = form.title.data
        posts.author = form.author.data
        posts.body = form.body.data
        db.session.commit()
        flash('Post is updated successfully', 'success')
        return redirect(url_for('posts.show_posts'))
    elif request.method == 'GET':
        form.title.data = posts.title
        form.author.data = posts.author
        form.body.data = posts.body
    return render_template('edit_post.html', form=form)


@posts.route('/delete_post/<int:id>', methods=['POST'])
@login_required
def delete_post(id):
    print('\n id is : \n', id)
    post = Posts.query.get_or_404(id)
    print('\n query post is : \n', post)
    print('\n post.author is : \n', post.author)
    print('\n current_user.username is : \n', current_user.username)
    if post.author != current_user.username:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('You post has been deleted!', 'success')
    return redirect(url_for('main.home'))


@posts.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Posts.query.filter_by(author=user.username).order_by(Posts.pub_date.desc()).paginate(page=page, per_page=5)
    page_paginates = Posts.query.paginate(page=page, per_page=5)
    return render_template('user_posts.html', user=user, posts=posts,page_paginates=page_paginates)



