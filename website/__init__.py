import os

from flask import Flask, redirect, url_for
from werkzeug.security import generate_password_hash


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'myCodeWars.sqlite'),
    )
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(app.instance_path, 'myCodeWars.sqlite')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Importing configurations and blueprints
    from website.models import db
    db.init_app(app)
    with app.app_context():
        if not os.path.isfile(app.config['DATABASE']):
            from website.models import User, Exercise
            db.create_all()
            admin_user = User(username="admin", password=generate_password_hash("admin"))
            db.session.add(admin_user)
            db.session.commit()

    app.register_blueprint(auth.bp)
    app.register_blueprint(user.bp)

    @app.route('/')
    def index():
        return redirect(url_for("user.main_page"))

    return app
