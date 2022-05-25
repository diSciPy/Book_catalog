from flask import render_template, request, flash, redirect, url_for, g, session
from flask_login import login_user, logout_user, login_required, current_user
from app import db, app
from app.authentication import authentication as at
from app.authentication.forms import RegistrationForm, LoginForm
from app.authentication.models import User, UserVerification, load_user
from app.authentication import send_email
from app.catalog import main
from datetime import datetime
from time import sleep
from flask_babel import Babel, _


#language switcher
@at.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', g.lang_code)


@at.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.lang_code = values.pop('lang_code')


@at.before_request
def fix_missing_csrf_token():
    if app.config['WTF_CSRF_FIELD_NAME'] not in session:
        if app.config['WTF_CSRF_FIELD_NAME'] in g:
            g.pop(app.config['WTF_CSRF_FIELD_NAME'])


@at.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@at.route('/register', methods=['GET', 'POST'])
def register_user():
    form = RegistrationForm()
    if current_user.is_authenticated:
        flash(_('You are already logged in'))
        return redirect(url_for('main.display_books'))
    if form.validate_on_submit():
        user = User.create_user(
            user=form.name.data,
            email=form.email.data,
            password=form.password.data)
        u_tkn = UserVerification.create_token(
            user_id=user.id)
        # email verification with SendGrid SMTP
        send_email.send_ver_email(user.user_email, user.user_name,
                                  url_for('authentication.user_verified', user_id=user.id,
                                          user_token=u_tkn.user_token), url_for('main.display_books'))
        flash(_('Registration is successful'))
        return redirect(url_for('authentication.do_the_login'))
    return render_template('registration.html', form=form)


@at.route('/user/<user_id>/verified/<user_token>')
def user_verified(user_id, user_token):
    u_token = UserVerification.query.filter_by(user_id=user_id).first()
    user = User.query.filter_by(id=user_id).first()
    if user.verified:
        flash(_('You are already verified please log in'))
        return redirect(url_for('main.display_books'))
    elif u_token.user_token == user_token and user.verified is False:
        u_token.verified_at = datetime.now()
        user = load_user(user_id)
        user.verified = True
        db.session.commit()
        return render_template('verified.html')
    else:
        return render_template('not-verified.html')


@at.route('/login', methods=['GET', 'POST'])
def do_the_login():
    if current_user.is_authenticated:
        flash(_('You are already logged in'))
        return redirect(url_for('main.display_books'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_email=form.email.data).first()
        if not user or not user.check_password(form.password.data):
            flash(_('Invalid Credentials. Please try again'))
            return redirect(url_for('authentication.do_the_login'))
        login_user(user, form.stay_loggedin.data)
        return redirect(url_for('main.display_books'))
    return render_template('login.html', form=form)


@at.route('/logout')
@login_required
def log_out_user():
    logout_user()
    return redirect(url_for('main.display_books'))


@at.app_errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
