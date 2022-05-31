
# Book catalog web app

Web app with book catalog:
- guests have read only permissions
- logged in users can edit catalog's content (CRUD in PostgreDB)



## Deployment

### AWS

To deploy this web app on AWS - TBD

```bash
  npm run deploy
```


## Run Locally

Clone the project

```bash
  git clone https://github.com/diSciPy/Book_catalog
```

Go to the project directory

```bash
  cd Book_catalog
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  python run.py
```


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

### For Local installation

`DEBUG = True`

`SECRET_KEY`

`SQLALCHEMY_DATABASE_URI`

#### Disable SSL for SSO
`OAUTHLIB_INSECURE_TRANSPORT = '1' `

`SQLALCHEMY_TRACK_MODIFICATIONS = True` 

#### For email verification
`SENDGRID_API_KEY`

#### Babel configs (for localizations)

`BABEL_TRANSLATION_DIRECTORIES`

`BABEL_DEFAULT_LOCALE`

#### For Google SSO

`GOOGLE_CLIENT_ID`

`GOOGLE_CLIENT_SECRET`


## Features

- Registration by email, Google SSO
- Localization (Babel)
- Email verification
- CRUD (PostgreSQL) for verified users


## Localization (Babel)

To enable Babel install dependancies from requirements.txt and add env vars to environment

### Add localization

#### Prepare files for Babel extraction

*In .py:*

"Some string" -> _("Some string")

"Some string" -> lazy_gettext("Some string")

*In .html:* ***(Enable Jinja)***

"Some string" -> {{_("Some string")}}

"Some string" -> {{lazy_gettext("Some string")}}

#### Extract files

```
$ mkdir locale
$ pybabel extract . -o app/locale/<name of the translations file>.pot

```

#### Prepare translations

In locale/<name of the translations file>.pot type in localized translations like:

```
msgid "This is a translatable string."
msgstr "This is localized translatable string"
```

#### Create translation catalog for specific locale

```
$ pybabel init -l <uk_UA - name of the locale> -i locale/<name of the translations file>.pot -d locale
```
Expected result:
```
creating catalog locale/uk_UA/LC_MESSAGES/messages.po based on locale/<name of the translations file>.pot
```

```
$ pybabel init
```
should be run per locale
In created .po file update msgstr according to locale translation

#### Update the localization

```
$ pybabel compile -d locale
```

Expected result:
```
compiling catalog locale/uk_UA/LC_MESSAGES/messages.po to locale/uk_UA/LC_MESSAGES/messages.mo
```

### Add localization to Jinja2 templates

```
$ pybabel extract -F babel.cfg -o locale/<name of the translations file>.pot
```

In created .pot file fill in the focalizations

Initialize <uk_UA> translations:
```
$ pybabel init -d locale -l uk_UA -i locale/<name of the translations file>.pot
```
Expected result:
```
creating catalog locale/uk_UA/LC_MESSAGES/messages.po based on locale/<name of the translations file>.pot
```

Compile translations file:
```
$ pybabel compile -d locale -l uk_UA
```
Expected result:
```
compiling catalog locale/uk_UA/LC_MESSAGES/messages.po to locale/uk_UA/LC_MESSAGES/messages.mo
```

### Update localization
If new lines of code (strings) were added, execute the following commands:

```
$ pybabel extract -F .\app\babel.cfg -k lazy_gettext -o .\app\locale\messages.pot --input-dirs=.\app

$ git diff
```
Delete existing .po and .mo files.
Run the following commands:

```
$ pybabel init -d .\app\locale -i .\app\locale\messages.pot -d .\app\locale -l uk_UA
$ pybabel compile -d .\app\locale
```





![Logo](file://app/static/favicon.ico)


## Acknowledgements

 - [Awesome tutorial to web app localization with Babel](https://phrase.com/blog/posts/i18n-advantages-babel-python)
 - [Official Flask-Babel docs](https://babel.pocoo.org/en/latest/cmdline.html)

