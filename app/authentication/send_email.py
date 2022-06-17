import os
import sendgrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
from flask_babel import Babel, _

load_dotenv()


def send_ver_email(to_emails, name, link, logo):
    message = Mail(
        from_email='4ign.literature@gmail.com',
        to_emails=to_emails,
        subject=_("Thanks for joining"),
        html_content='<a>Verification email</a>')
    message.dynamic_template_data = {
        'subject': _('Verification of email'),
        'name': name,
        'link': f'https://foreign-literature.pp.ua{link}',
        'logo': f'{logo}'
    }
    message.template_id = 'd-a5bfd1b931aa4c61a4ed13fca9b29a94'

    try:
        sendgrid_client = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sendgrid_client.send(message)
        print(response.status_code)
    except Exception as e:
        print(e.message)
