from flask import Blueprint

authentication = Blueprint('authentication', __name__, template_folder='templates', url_prefix='/<lang_code>',
                           static_folder='../static', static_url_path='/static')

from app.authentication import routes
