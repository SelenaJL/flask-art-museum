import os

from flask import Flask, url_for


# application factory function
def create_app(test_config=None):
    # create Flask instance with config files relative to the instance folder located outside the flaskr package
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev', # protect data
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'), # path to save SQLite database file
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
	# overrides the deflaut configs, use to set a real SECRET_KEY
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # import and register database
    from . import db
    db.init_app(app)

    # import and register blueprints
    from . import auth
    app.register_blueprint(auth.bp)
    from . import blog
    app.register_blueprint(blog.bp)
    # the blog blueprint doesn't have a url_prefix and will be the main index of the app
    app.add_url_rule('/', endpoint='index') # 'index' and 'blog.index' are both endpoints for the same URL '/'

    # an example page to test with
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
