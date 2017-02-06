from datetime import timedelta
import json
import logging
import os
from logger import logging_config

from flask import request, render_template, Response, url_for
from flask.ext.script import Manager

from application.service.deed_api import make_deed_api_client
from .health.views import health
from .deed.searchdeed.views import searchdeed
from .borrower.views import borrower_landing
from .digital_mortgage_flask import DigitalMortgageFlask


logging_config.setup_logging()
LOGGER = logging.getLogger(__name__)
LOGGER.info("Starting the server")


def create_manager(deed_api_client=make_deed_api_client()):
    app = DigitalMortgageFlask(__name__,
                               template_folder='templates',
                               static_folder='assets/.dist',
                               static_url_path='/static'
                               )

    app.config.from_pyfile('config.py')

    manager = Manager(app)
    app.url_map.strict_slashes = False

    setattr(searchdeed, 'deed_api_client', deed_api_client)
    setattr(borrower_landing, 'deed_api_client', deed_api_client)

    app.register_blueprint(health, url_prefix='/health')
    app.register_blueprint(searchdeed)
    app.register_blueprint(borrower_landing)
    app.secret_key = app.config['APP_SECRET_KEY']

    app.permanent_session_lifetime = timedelta(minutes=20)

    return manager


manager = create_manager()


def request_wants_json():
    best = request.accept_mimetypes \
        .best_match(['application/json', 'text/html'])
    return best == 'application/json' and \
        request.accept_mimetypes[best] > \
        request.accept_mimetypes['text/html']


@manager.app.route('/server-error', methods=['GET'])
def render_server_error():
    return render_template('503.html'), 500


@manager.app.route('/page-not-found', methods=['GET'])
def render_page_not_found():
    return render_template('404.html'), 404


@manager.app.errorhandler(Exception)
def unhandled_exception(e):
    LOGGER.error("Unhandled Exception: '%s'", (e,), exc_info=True)
    if request_wants_json():
        error_redirect = {'error': True,
                          'redirect': url_for('render_server_error', error=True)}
        return Response(json.dumps(error_redirect), 500)
    return render_template('503.html'), 500


@manager.app.errorhandler(404)
def page_not_found(e):
    LOGGER.error('Page not found: %s', (e,), exc_info=True)
    if request_wants_json():
        error_redirect = {'error': True,
                          'redirect': url_for('render_page_not_found', error=True)}
        return Response(json.dumps(error_redirect), 404)
    return render_template('404.html'), 404


@manager.app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    """Cachebusting

    Use the last updated timestamp from the file on disk to perform cachebusting duties.
    This forces browsers to download new versions of files when they change.
    """
    if endpoint == 'static':
        filename = values.get('filename', None)

        if filename:
            file_path = os.path.join(manager.app.root_path, manager.app.static_folder, filename)
            values['cache'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)
