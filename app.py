from pathlib import Path
from flask import Flask

from database import close_db, init_database
from auth_routes import auth_bp
from dashboard_routes import dashboard_bp
from report_routes import report_bp

BASE_DIR = Path(__file__).resolve().parent


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "change-this-secret-key-before-production"
    app.config["DATABASE"] = str(BASE_DIR / "database.db")
    app.config["UPLOAD_FOLDER"] = str(BASE_DIR / "uploads")
    app.config["REPORT_FOLDER"] = str(BASE_DIR / "reports")
    app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024

    Path(app.config["UPLOAD_FOLDER"]).mkdir(exist_ok=True)
    Path(app.config["REPORT_FOLDER"]).mkdir(exist_ok=True)

    init_database(app.config["DATABASE"])
    app.teardown_appcontext(close_db)

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(report_bp)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
