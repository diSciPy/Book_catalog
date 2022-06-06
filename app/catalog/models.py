from app import db
import sqlalchemy_utils
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import JSON
from flask import g, request
from datetime import datetime
import json


# table localization
class Publication(db.Model):
    __tablename__ = 'publication'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.JSON, nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"The Publisher Name is {self.name['en']}"


##to add new published to table
# from <name of the file> import <name of the class>
# create object {oracle=Publication(103,"Oracle Inc")}
##add object to DB -> if one ->db.session.add(oracle) if many->db.session.add_all([Ababagalamaga,KSD,paramount,oracle])
## save changes -> db.session.commit()

class Book(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.JSON, nullable=False)
    author = db.Column(db.JSON)
    avr_rating = db.Column(db.Float)
    format = db.Column(db.JSON)
    image = db.Column(db.JSON)
    num_pages = db.Column(db.Integer)
    pub_date = db.Column(db.DateTime, default=datetime.utcnow())

    # Relationship
    pub_id = db.Column(db.Integer, db.ForeignKey('publication.id'))

    def __init__(self, title, author, avr_rating, book_format, image, num_pages, pub_id):
        self.title = title
        self.author = author
        self.avr_rating = avr_rating
        self.format = book_format
        self.image = image
        self.num_pages = num_pages
        self.pub_id = pub_id

    def __repr__(self):
        return f"{self.title} by {self.author['en']}"

