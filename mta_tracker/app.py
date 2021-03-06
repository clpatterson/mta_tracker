from flask import Flask
from mta_tracker.extensions import api, db

def create_app(settings_override=None):
    """
    Create a Flask application using the app factory pattern.

    :param settings_override: Override settings
    :return: Flask app
    """
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object('config.settings')
    app.config.from_pyfile('settings.py', silent=True)

    if settings_override:
        app.config.update(settings_override)
    
    from mta_tracker.resources.subway.lines import LineStatus, LineUptime

    # Register routes for api resources
    url_base = '/mta_tracker/api/v1.0/'
    api.add_resource(LineStatus, f'{url_base}subway/lines/status', endpoint='status')
    api.add_resource(LineUptime, f'{url_base}subway/lines/uptime', endpoint='uptime')

    extensions(app) # must initialize api after adding routes
    
    return app

def extensions(app):
    """
    Register 0 or more extensions (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """
    api.init_app(app)
    db.init_app(app)

    return None