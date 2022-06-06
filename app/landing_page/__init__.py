from flask import Blueprint

landing_page = Blueprint('landing_page', __name__, template_folder='templates', static_folder='../static',
                         static_url_path='/static')

from app.landing_page import routes
