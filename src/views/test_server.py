import os

from flask import request, jsonify, render_template
from sqlalchemy import text

from src.controller.admin_controller import upload_file_controller
from src.controller.gpt_controller import ai_command_controller
from src.controller.home_page_controller import home_page_controller
from src.controller.token_evaluation_controller import token_evaluation_controller, token_occurrences_controller, \
    fetch_vector_db_info_controller, fetch_sql_db_info_controller
from src.tokenization.tokenization import Tokenization
from src.vector_db.vectordb import VectorDb
from src.views import create_app, db

app = create_app()

# Directory where uploaded files will be stored
UPLOAD_FOLDER = 'data_files'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route('/', methods=['GET', 'POST'])
def index():
    return home_page_controller(request)


@app.route('/submit-ai-command', methods=['POST'])
def ai_command():
    return ai_command_controller(request)


@app.route('/token_evaluation/', methods=['POST', 'GET'])
def token_evaluation():
    return token_evaluation_controller(request)


def test_vect_post():
    tokenization = Tokenization(file_path="./data_files/input/p4.csv")

    # vector_db = VectorDb()
    # print("...................", tokenization.processed_data)
    # vector_db.post_data(tokenization.processed_data)


@app.route('/token_occurrences/')
def fetch_unique_tokens():
    return token_occurrences_controller(request)


@app.route('/vector-db-details/')
def fetch_vector_db_info():
    return fetch_vector_db_info_controller(request)


@app.route('/sql-db-details/')
def fetch_sql_db_info():
    return fetch_sql_db_info_controller(request)



@app.route('/admin_controll/')
def admin_controll():
    return  render_template('admin_control.html')
@app.route('/upload_file', methods=['POST'])
def upload_file():
    return upload_file_controller(request, UPLOAD_FOLDER)


from sqlalchemy import text
from flask import jsonify


@app.route('/clear_sql_db', methods=['POST'])
def clear_sql_db():
    try:
        # Drop all tables
        db.drop_all()

        # Recreate all tables
        db.create_all()

        db.session.commit()  # Commit the changes
        return jsonify({'status': 'success', 'message': 'SQL Database cleared successfully'})

    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        return jsonify({'status': 'error', 'message': str(e)})



@app.route('/clear_vector_db', methods=['POST'])
def clear_vector_db():
    # Add logic to clear the vector database here
    return jsonify({'status': 'success', 'message': 'Vector Database cleared successfully'})
