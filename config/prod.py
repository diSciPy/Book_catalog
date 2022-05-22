import os
import re

DEBUG = os.getenv( 'DEBUG', False )

#to comply with heroku connection to postgre SQL DB
uri = os.getenv('DATABASE_URL')
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
#SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv( 'SQLALCHEMY_TRACK_MODIFICATIONS', False )
LANGUAGES = ['en', 'uk_UA']