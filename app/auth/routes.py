import requests
from flask import render_template, flash, redirect, url_for, request, current_app
from app.auth.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user
import sqlalchemy as sa
from app.models import User
from urllib.parse import urlsplit
from app.auth import bp
from app import db, verify_captcha


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile', username=current_user.username))
    form = LoginForm()
    if form.validate_on_submit():
        # Get user from database
        user = db.session.scalar(sa.select(User).where(User.username == form.username.data))
        # If user exists in database (so the user object isn't empty) check password
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'error')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(url_for('main.index'))
    return render_template('login.html', title='Sign In', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('profile', username=current_user.username))
    form = RegistrationForm()
    if form.validate_on_submit():
        # CAPTCHA validation
        captcha_response = request.form.get('g-recaptcha-response')
        captcha_valid, error_message = verify_captcha(captcha_response)
        if not captcha_valid:
            return redirect(url_for('auth.register'))

        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        login_user(user, remember=True)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(url_for('main.profile', username=current_user.username))
    return render_template('registration.html', title='Register', form=form, current_app=current_app)