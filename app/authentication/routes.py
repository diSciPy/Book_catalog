import json

from flask import render_template, request, flash, redirect, url_for, g, session, send_from_directory
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.authentication import authentication as at
from app.authentication.forms import RegistrationForm, LoginForm
from app.authentication.models import User, UserVerification, load_user
from app.authentication import send_email
from app.catalog import main
from datetime import datetime
from time import sleep
from flask_babel import Babel, _
from oauthlib.oauth2 import WebApplicationClient
import requests
import os

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)


#SSO OAuth 2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)


def get_google_provide_cfg():
    try:
        return requests.get(GOOGLE_DISCOVERY_URL).json()
    except:
        return 404


#language switcher
@at.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', g.lang_code)


@at.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.lang_code = values.pop('lang_code')

#
# @at.before_request
# def fix_missing_csrf_token():
#     if session['csrf_token'] not in session:
#         if session['csrf_token'] in g:
#             g.pop(session['csrf_token'])


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


@at.route('/login/sso/google')
def google_login():
    if current_user.is_authenticated:
        flash(_('You are already logged in'))
        return redirect(url_for('main.display_books'))
    # URL for Google login
    google_provider_cfg = get_google_provide_cfg()
    authorization_endpoint = google_provider_cfg.get('authorization_endpoint')
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=['openid', 'email', 'profile']
    )
    return redirect(request_uri)


@at.route('/login/sso/google/callback')
def google_callback():
    # get auth code from Google
    code = request.args.get('code')
    # found Google URL to send tokens to access user info
    google_provider_cfg = get_google_provide_cfg()
    token_endpoint = google_provider_cfg['token_endpoint']
    # prepare request to send tokens
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )
    # parse tokens
    client.parse_request_body_response(json.dumps(token_response.json()))
    #get user info with tokens
    userinfo_endpoint = google_provider_cfg['userinfo_endpoint']
    uri, headers, body = client.add_token((userinfo_endpoint))
    userinfo_response = requests.get(uri, headers=headers, data=body)
    # check Google user's email is verified
    if userinfo_response.json().get('email_verified'):
        users_email = userinfo_response.json()['email']
        users_name = userinfo_response.json()['given_name']
        users_lastname = userinfo_response.json()['family_name']
        users_unique_id = userinfo_response.json()['sub']
    else:
        return _("User email not available or not verified by Google"), 400
    # create user in DB
    user = User.query.filter_by(user_email=users_email).first()
    if not user:
        user = User.create_user(
            user='_'.join([users_name, users_lastname]),
            email=users_email,
            password=users_unique_id,
            verified=True
        )
    # login user
    login_user(user, True)
    return redirect(url_for('main.display_books'))


@at.route('/logout')
@login_required
def log_out_user():
    logout_user()
    return redirect(url_for('main.display_books'))


@at.app_errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
