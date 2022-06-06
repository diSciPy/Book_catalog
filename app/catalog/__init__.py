#venv/app/catalog

from flask import Blueprint

main = Blueprint('main', __name__, template_folder='templates', url_prefix='/<lang_code>', static_folder='../static',
                 static_url_path='/static')

from app.catalog import routes

