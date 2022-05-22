from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.authentication.models import User
from flask_babel import Babel, _, lazy_gettext

# explanation to validatiors:
# 1. field cannot be empty
# 2. length of the input data - (not shorter than, not longer than, message displayed if validation failed)
# 3. validation of correct email format

def email_exists(form, field):
    email = User.query.filter_by(user_email=field.data).first()
    if email:
        raise ValidationError(_('Email Already Exists'))


class RegistrationForm(FlaskForm):
    name = StringField(lazy_gettext('Name'),
                       validators=[DataRequired(), Length(3, 15, message=_('Name should be between 3 to 15 characters'))])
    email = StringField(lazy_gettext('E-mail'), validators=[DataRequired(), Email(), email_exists])
    password = PasswordField(lazy_gettext('Password'),
                             validators=[DataRequired(), Length(5), EqualTo(_('confirm'), message=_("passwords must match"))])
    confirm = PasswordField(lazy_gettext('Confirm'), validators=[DataRequired()])
    submit = SubmitField(lazy_gettext('Register'))


class LoginForm(FlaskForm):
    email = StringField(lazy_gettext('E-mail'), validators=[DataRequired(), Email()])
    password = PasswordField(lazy_gettext('Password'), validators=[DataRequired()])
    stay_loggedin = BooleanField(lazy_gettext('stay logged-in'))
    submit = SubmitField(lazy_gettext('Log in'))
