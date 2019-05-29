import os

from redis import Redis

from flask import Flask, jsonify
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_debugtoolbar import DebugToolbarExtension
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# instantiate the extensions

login_manager = LoginManager()
bcrypt = Bcrypt()
toolbar = DebugToolbarExtension()
bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()

redis = Redis(host='redis', port=6379, db=0)


def create_base_app():
    # instantiate the app
    from project.server.model.user import User
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'danger'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter(User.id == int(user_id)).first()

    app = Flask(
        __name__,
        template_folder='../client/templates',
        static_folder='../client/static'
    )
    app.secret_key = 'super secret string'  # Change this!

    app_settings = os.getenv(
        'APP_SETTINGS', 'project.server.config.DevelopmentConfig')
    app.config.from_object(app_settings)

    login_manager.init_app(app)
    bcrypt.init_app(app)
    toolbar.init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # register blueprints
    from project.server.auth.views import auth_blueprint
    from project.server.group.views import group_blueprint
    from project.server.members.views import members_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(group_blueprint)
    app.register_blueprint(members_blueprint)

    return app


def create_app(script_info=None):

    app = create_base_app()

    # error handlers
    @app.errorhandler(401)
    def unauthorized_page(error):
        return jsonify({"error": {}}), 401

    @app.errorhandler(403)
    def forbidden_page(error):
        return jsonify({"error": {}}), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return jsonify({"error": {}}), 404

    @app.errorhandler(500)
    def server_error_page(error):
        return jsonify({"error": {}}), 500

    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}

    return app
