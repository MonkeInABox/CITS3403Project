import threading
from flask import render_template, flash, redirect, url_for, request, current_app
from app.auth.forms import LoginForm, RegistrationForm, UsernameForm
from app.main.forms import SearchForm
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from sqlalchemy.sql.expression import collate
from app.models import User
from urllib.parse import urlsplit
from app.auth import bp
from app import db, mail
from flask_mail import Message

@bp.context_processor
def heading():
    form = SearchForm()
    return dict(form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile', username=current_user.username))
    form = LoginForm()
    if form.validate_on_submit():
        # Get user from database
        user = db.session.scalar(sa.select(User).where(collate(User.username, 'NOCASE') == form.username.data))
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

@bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    email = User.confirm_password_reset_token(token)
    
    if not email:
        # Token is invalid or has expired
        return render_template('invalid_token.html', )
    
    # If valid, handle the password reset logic (like showing a form for a new password)
    if request.method == 'POST':
        new_password = request.form.get('new_password')
        user = User.query.filter_by(email=email).first()
        user.set_password(new_password)
        db.session.commit()
        flash('Password has been reset successfully.', 'success')  # Flash success message
        return redirect(url_for('main.index'))  # Redirect to main.index
    
    # Render a form for the user to enter their new password
    return render_template('passwordreset.html')

def send_email_async(app, msg):
    with app.app_context():
        mail.send(msg)

@bp.route('/send-reset/', defaults={'username': None}, methods=['POST', 'GET'])
@bp.route('/send-reset/<username>', methods=['POST', 'GET'])
def send_reset(username):
    if not current_user.is_authenticated and not username:
        # If there's no logged-in user and no username, ask for it
        form = UsernameForm()
        if form.validate_on_submit():
            # Redirect to the route with the username
            return redirect(url_for('auth.send_reset', username=form.username.data))
        return render_template('enter_username.html', form=form)  # Create a template to collect the username

    # Now handle the case when we have a username (either from parameter or from current_user)
    if username:
        user = db.first_or_404(sa.select(User).where(collate(User.username, 'NOCASE') == username))
    else:
        user = current_user
    
    token = User.generate_password_reset_token(user.email)
    reset_url = url_for('auth.reset_password', token=token, _external=True)  # Full URL

    msg = Message(
        "Password Reset Request",
        sender=current_app.config['MAIL_USERNAME'],
        recipients=[user.email],
        body=f"To reset your password, click the following link (it will expire in 1 hour): {reset_url}"
    )

    threading.Thread(target=send_email_async, args=(current_app._get_current_object(), msg)).start()

    flash('If the username provided exists - a password reset email will be sent to the email address.', 'info')
    return redirect(url_for('auth.login'))  # Redirect after sending the email
