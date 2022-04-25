import os

from flask import Flask
from sales import db, core, data


def create_app(test_config=None):
    """create and configure the app"""

    print("Creating and configuring the app ...")
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'sales.sqlite'),
    )

    if test_config is not None:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    print("Initializing the database ...")
    # register the database commands
    db.init_app(app)

    # apply the core blueprint to the app
    app.register_blueprint(core.bp)
    app.add_url_rule('/', endpoint='index')

    print("All set.")
    return app
