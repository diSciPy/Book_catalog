from datetime import datetime
from app import db, bcrypt
from flask_login import UserMixin
from app import login_manager
import secrets
import requests


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20))
    user_email = db.Column(db.String(60), unique=True, index=True)
    user_password = db.Column(db.String(80))
    registration_date = db.Column(db.DateTime, default=datetime.now)
    verified = db.Column(db.Boolean, default=False)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.user_password, password)

    # clasmethods belong to a class but are not associated with any class instance
    @classmethod
    def create_user(cls, user, email, password, verified=False):
        user = cls(user_name=user,
                   user_email=email,
                   user_password=bcrypt.generate_password_hash(password).decode('utf-8'),
                   verified=verified)

        db.session.add(user)
        db.session.commit()
        return user


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class UserVerification(db.Model):
    __tablename__ = 'tokens'

    id = db.Column(db.Integer, primary_key=True)
    user_token = db.Column(db.String(120))
    verified_at = db.Column(db.DateTime)

    # PK_FK relationship
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @classmethod
    def create_token(cls, user_id):
        u_tkn = cls(user_token=secrets.token_urlsafe(32),
                    user_id=user_id)
        db.session.add(u_tkn)
        db.session.commit()
        return u_tkn

