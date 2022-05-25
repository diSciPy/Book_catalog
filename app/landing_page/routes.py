from flask import render_template, request, flash, redirect, url_for, g, session
from app import db#, app
from app.landing_page import landing_page as lp
from app.catalog import main
import os
from flask import send_from_directory


#language switcher
@lp.route('/')
def switch_lang_code():
    values.setdefault('lang_code', 'en')
    return redirect(url_for('main.display_books', lang_code='en'))


@lp.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
