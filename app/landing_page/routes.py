from flask import render_template, request, flash, redirect, url_for, g, session, send_from_directory
from app import db, get_project_root
from app.landing_page import landing_page as lp
from app.catalog import main
import os
from flask import send_from_directory


@lp.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.get_project_root, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


#language switcher
@lp.route('/')
def switch_lang_code():
    g.lang_code = 'en'
    return redirect(url_for('main.display_books'))