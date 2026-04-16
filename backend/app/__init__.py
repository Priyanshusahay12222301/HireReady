from flask import Flask
from sqlalchemy import text

from config import CONFIG_MAP

from .extensions import bcrypt, cors, db, login_manager, migrate


def ensure_users_gender_column():
    columns = db.session.execute(text("PRAGMA table_info(users)")).fetchall()
    existing = {row[1] for row in columns}
    if "gender" in existing:
        return

    # Keep local SQLite dev DB compatible when model adds a new nullable column.
    db.session.execute(text("ALTER TABLE users ADD COLUMN gender VARCHAR(20)"))
    db.session.commit()


def create_app(env_name: str = "development") -> Flask:
    app = Flask(__name__)
    app.config.from_object(CONFIG_MAP.get(env_name, CONFIG_MAP["development"]))

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})

    from .routes import register_blueprints

    register_blueprints(app)

    with app.app_context():
        db.create_all()
        if str(app.config.get("SQLALCHEMY_DATABASE_URI", "")).startswith("sqlite"):
            ensure_users_gender_column()

    return app
