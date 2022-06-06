from app import create_app, db

#if __name__=="__main__":
flask_app = create_app('dev')
with flask_app.app_context():
    db.create_all()
    # if not User.query.filter_by(user_name='harry').first():
    #     User.create_user(user='harry',
    #                      email='harry@potter.com',
    #                      password='secret')
    #flask_app.run(debug=True, host="0.0.0.0")

