import os
import re

DEBUG = os.getenv( 'DEBUG', False )

#to comply with heroku connection to postgre SQL DB
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)
SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv( 'SQLALCHEMY_TRACK_MODIFICATIONS', False )
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
LANGUAGES = ['en', 'uk_UA']
BABEL_TRANSLATION_DIRECTORIES = os.getenv('BABEL_TRANSLATION_DIRECTORIES')