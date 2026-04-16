from flask import Flask

from .applications import applications_bp
from .auth import auth_bp
from .dashboard import dashboard_bp
from .health import health_bp
from .interviews import interviews_bp
from .jobs import jobs_bp
from .mock_tests import mock_tests_bp
from .questions import questions_bp


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(health_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(questions_bp, url_prefix="/api")
    app.register_blueprint(mock_tests_bp, url_prefix="/api")
    app.register_blueprint(jobs_bp, url_prefix="/api")
    app.register_blueprint(interviews_bp, url_prefix="/api")
    app.register_blueprint(applications_bp, url_prefix="/api")
    app.register_blueprint(dashboard_bp, url_prefix="/api")
