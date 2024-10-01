
from flask import request

from src.controller.gpt_controller import ai_command_controller
from src.controller.home_page_controller import home_page_controller
from src.controller.token_evaluation_controller import token_evaluation_controller, token_occurrences_controller, \
    fetch_vector_db_info_controller, fetch_sql_db_info_controller
from src.tokenization.tokenization import Tokenization
from src.vector_db.vectordb import VectorDb
from src.views import create_app
app = create_app()
@app.route('/', methods=['GET', 'POST'])
def index():
    return home_page_controller(request)

@app.route('/submit-ai-command', methods=['POST'])
def ai_command():
    return ai_command_controller(request)

@app.route('/token_evaluation/',methods=['POST','GET'])
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