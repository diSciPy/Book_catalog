from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, IntegerField, SelectField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms.validators import DataRequired
from flask_babel import Babel, _, lazy_gettext
from app.catalog.models import Publication


class EditBookForm(FlaskForm):
    title_en = StringField(lazy_gettext('Title (english)'))
    title_ua = StringField(lazy_gettext('Title (ukrainian)'))
    format_en = SelectField(lazy_gettext('Format (english)'),
                            choices=[('hardcover', 'hardcover'), ('paperback', 'paperback'), ('eBook', 'eBook')])
    format_ua = SelectField(lazy_gettext('Format (ukrainian)'),
                            choices=[('палітурка', 'палітурка'), ('м`яка обкладинка', 'м`яка обкладинка'), ('електронна книга', 'електронна книга')])

    author_en = StringField(lazy_gettext('Author (english)'))
    author_ua = StringField(lazy_gettext('Author (ukrainian)'))
    num_pages = IntegerField(lazy_gettext('Pages'))
    cover_en = FileField(lazy_gettext('Book cover (english)'), validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], lazy_gettext('Images only!'))
    ])
    cover_ua = FileField(lazy_gettext('Book cover (ukrainian)'), validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], lazy_gettext('Images only!'))
    ])
    submit = SubmitField(lazy_gettext('Update'))


class CreateBookForm(FlaskForm):
    title_en = StringField(lazy_gettext('Title (english)'), validators=[DataRequired()])
    title_ua = StringField(lazy_gettext('Title (ukrainian)'), validators=[DataRequired()])
    author_en = StringField(lazy_gettext('Author (english)'), validators=[DataRequired()])
    author_ua = StringField(lazy_gettext('Author (ukrainian)'), validators=[DataRequired()])
    avr_rating = FloatField(lazy_gettext('Rating'), validators=[DataRequired()])
    format_en = SelectField(lazy_gettext('Format (english)'),
                            choices=['hardcover', 'paperback', 'eBook'],
                            validators=[DataRequired()])
    format_ua = SelectField(lazy_gettext('Format (ukrainian)'),
                            choices=['палітурка', 'м`яка обкладинка', 'електронна книга'],
                            validators=[DataRequired()])
    img_url_en = StringField(lazy_gettext('Image (english)'), validators=[DataRequired()])
    img_url_ua = StringField(lazy_gettext('Image (ukrainian)'), validators=[DataRequired()])
    num_pages = IntegerField(lazy_gettext('Pages'), validators=[DataRequired()])
    publisher = SelectField(lazy_gettext('Publisher'), validate_choice=True, coerce=int)
    submit = SubmitField(lazy_gettext('Create'))
