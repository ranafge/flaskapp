from flask import Blueprint
from flaskapp import db, bcrypt
from flask import render_template, request, flash, redirect, url_for
from flaskapp.users.forms import (RegistrationForm, LoginForm,
                                  RequestResetForm, ResetPasswordForm
                                 )
from flaskapp.users.utils import send_reset_email
from flaskapp.models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.urls import url_parse

users = Blueprint('users', __name__)


@users.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=name, email=email, username=username, password=password)
        db.session.add(user)
        db.session.commit()
        flash('You have registered successfully. You may login in now.', 'success')
        return redirect(url_for('main.home'))

    return render_template('register.html', form=form)


@users.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not bcrypt.check_password_hash(user.password, form.password.data):
            flash('Invalid User email or Password,Please Check Caps Lock', 'Fail')
            return redirect(url_for('users.login'))

        flash('You have successfully login', 'success')
        login_user(user)

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.dashboard')
        return redirect(next_page)
    return render_template('login.html', form=form)


@users.route("/reset_password", methods=['POST', 'GET'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been send to reset password')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset password', form=form)


@users.route('/reset_password/<token>', methods=['POST', 'GET'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    print('This is an invalid or expire token, Because user is or token :', user)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = password
        db.session.commit()
        flash('You password updated.', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', token=token, title='Reset Password', form=form)


@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

