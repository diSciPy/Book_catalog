import random
from app.catalog import main
from app import db, get_project_root
from app.catalog.models import Book, Publication
from flask import render_template, flash, request, redirect, url_for, g, send_from_directory
from flask_login import login_required, current_user
from app.catalog.forms import EditBookForm, CreateBookForm, upload_image
from flask_paginate import Pagination, get_page_parameter
from flask_babel import Babel, _
from sqlalchemy.sql.expression import func
from sqlalchemy.orm.attributes import flag_modified
from werkzeug.utils import secure_filename
from PIL import Image, UnidentifiedImageError
import os


ROWS_PER_PAGE = 6


@main.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', g.lang_code)


@main.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.lang_code = values.pop('lang_code')


# @main.before_request
# def fix_missing_csrf_token():
#     if app.config['WTF_CSRF_FIELD_NAME'] not in session:
#         if app.config['WTF_CSRF_FIELD_NAME'] in g:
#             g.pop(app.config['WTF_CSRF_FIELD_NAME'])


@main.route('/')
@main.route('/<int:page>')
def display_books(page=1):
    try:
        #Set the pagination configuration
        search = False
        q = request.args.get('q')
        if q:
            search = True

        publisher = Publication.query.order_by(Publication.id.asc()).all()
        books = Book.query.order_by(Book.id.asc()).paginate(page=page, per_page=ROWS_PER_PAGE,
                                                            error_out=False, max_per_page=ROWS_PER_PAGE)
        user = current_user.is_authenticated
        return render_template('home.html', books=books, publisher=publisher, user=user, lang_code=g.lang_code)
    except KeyError:
        return redirect('/en')


@main.route('/display/publisher/<int:publisher_id>')
def display_publisher(publisher_id):
    publisher = Publication.query.filter_by(id=publisher_id).first()
    publisher_books = Book.query.filter_by(pub_id=publisher_id).all()
    return render_template('publisher.html', publisher=publisher, publisher_books=publisher_books, lang_code=g.lang_code)


@main.route('/book/delete/<int:book_id>', methods=['GET', 'POST'])
@login_required
def delete_book(book_id):
    book = Book.query.get(book_id)
    if request.method == "POST":
        db.session.delete(book)
        db.session.commit()
        flash(_('book {} has been successfully deleted from catalog').format(book.title[g.lang_code]))
        return redirect(url_for('main.display_books'))
    return render_template('delete_book.html', book=book, book_id=book.id, lang_code=g.lang_code)


@main.route('/edit/book/<int:book_id>', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    book = Book.query.filter_by(id=book_id).first()
    form = EditBookForm(obj=book, data={'title_en': book.title['en'], 'title_ua': book.title['uk_UA'],
                                        'format_en': book.format['en'], 'format_ua': book.format['uk_UA'],
                                        'author_en': book.author['en'], 'author_ua': book.author['uk_UA']})
    # #populate imgs with default values from db
    # for img in form.cover_en, form.cover_ua:
    #     if img.name[-2:] == 'ua':
    #         path = book.image['uk_UA']
    #     else:
    #         path = book.image[img.name[-2:]]
    #     try:
    #         img = Image.open(os.path.join(get_project_root(), 'static', 'img', path))
    #     except (FileNotFoundError, UnidentifiedImageError):
    #         img = Image.open(os.path.join(get_project_root(), 'static', 'img', 'broken_img.png'))
    #     img.close()
    if request.method == 'POST' and form.validate_on_submit():
        form.process(formdata=request.form)

        #upload book cover

        book.title['en'] = form.title_en.data
        book.title['uk_UA'] = form.title_ua.data
        book.format['en'] = form.format_en.data
        book.format['uk_UA'] = form.format_ua.data
        book.author['en'] = form.author_en.data
        book.author['uk_UA'] = form.author_ua.data
        book.num_pages = form.num_pages.data
        for img in form.cover_en, form.cover_ua:
            if request.files[img.name]:
                cover = upload_image(request.files[img.name], form.title_en.data, img.name[-2:])
                if img.name[-2:] == 'en':
                    book.image[img.name[-2:]] = cover.filename
                    flag_modified(book, f"image")
                else:
                    book.image['uk_UA'] = cover.filename
                    flag_modified(book, f"image")

        #update DB fields
        for fieldname, value in form.data.items():
            if fieldname in ('submit', 'csrf_token') or fieldname[:-3] == 'cover':
                continue
            elif len(str(value)) > 0 and fieldname == 'num_pages':
                flag_modified(book, f"{fieldname}")
            elif len(str(value)) > 0:
                flag_modified(book, f"{fieldname[:-3]}")
            else:
                break

        db.session.commit()
        flash(_('Book {} by {} has been edited successfully').format(book.title[g.lang_code], book.author[g.lang_code]))
        return redirect(url_for('main.display_books'))
    return render_template('edit_book.html', form=form, title=book.title[g.lang_code])


@main.route('/create/book/<int:pub_id>', methods=['GET', 'POST'])
@login_required
def create_book(pub_id):
    publisher_book = Publication.query.get(pub_id)
    form = CreateBookForm(lang_code=g.lang_code, data={'publisher': publisher_book})
    form.publisher.choices = [(pub.id, pub.name[g.lang_code]) for pub in Publication.query.order_by('id').all()]
    #form.publisher.data = pub_id  # prepopulates pub_name
    if form.validate_on_submit():
        img_en_filename, img_ua_filename = upload_image(request.files['cover_en'],
                                                        request.files['cover_ua'],
                                                        form.title_en.data)
        book = Book(title=dict({"en": form.title_en.data, "uk_UA": form.title_ua.data}),
                    author=dict({"en": form.author_en.data, "uk_UA": form.author_ua.data}),
                    avr_rating=form.avr_rating.data,
                    book_format=dict({"en": form.format_en.data, "uk_UA": form.format_ua.data}),
                    image=dict({"en": img_en_filename, "uk_UA": img_ua_filename}),
                    num_pages=form.num_pages.data, pub_id=int(form.publisher.data))
        db.session.add(book)
        db.session.commit()
        flash(_('Book "{}" by {} has been successfully added to catalog').format(book.title[g.lang_code], book.author[g.lang_code]))
        return redirect(url_for('main.display_publisher', publisher_id=pub_id, lang_code=g.lang_code))
    return render_template('create_book.html', form=form, pub_id=pub_id, publisher=publisher_book, lang_code=g.lang_code)
