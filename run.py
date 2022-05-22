from app import create_app, db
from app import app as application

if __name__ == '__main__':

    application = create_app('prod')
    with application.app_context():
        db.create_all()
        # if not User.query.filter_by(user_name='harry').first():
        #     User.create_user(user='harry',
        #                      email='harry@potter.com',
        #                      password='secret')
    application.run()

##gunicorn - http server web will be run