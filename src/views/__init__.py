# test_server/__init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
file = '../sql_db/database.db'
def create_app():
    app = Flask(__name__)
    # Path to SQLite database file
    db_file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), file)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_file_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Initialize SQLAlchemy with the app
    db.init_app(app)
    # Import and register blueprints or views
    with app.app_context():
        pass
    return app
