from app import get_project_root
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, IntegerField, SelectField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms.validators import DataRequired
from flask_babel import Babel, _, lazy_gettext
from app.catalog.models import Publication
import os


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
    cover_en = FileField(lazy_gettext('Book cover (english)'), validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], lazy_gettext('Images only!')), DataRequired()
    ])
    cover_ua = FileField(lazy_gettext('Book cover (ukrainian)'), validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], lazy_gettext('Images only!')), DataRequired()
    ])
    num_pages = IntegerField(lazy_gettext('Pages'), validators=[DataRequired()])
    publisher = SelectField(lazy_gettext('Publisher'), validate_choice=True, coerce=int)
    submit = SubmitField(lazy_gettext('Create'))


# args - form.data fields
def upload_image(cover, book_title_en, locale):
    cover.filename = secure_filename(locale +'_' + '_'.join(book_title_en.split())+'.jpg')
    cover.save(os.path.join(get_project_root(), 'static', 'img', cover.filename))
    return cover
