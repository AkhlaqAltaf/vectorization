
from flask import Flask, request

from src.controller.gpt_controller import ai_command_controller
from src.controller.home_page_controller import home_page_controller
from src.controller.token_evaluation_controller import token_evaluation_controller, token_occurrences_controller, \
    fetch_vector_db_info_controller
from src.db.tokenization import Tokenization
from src.db.vectordb import VectorDb

app = Flask(__name__)


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

    vector_db = VectorDb()
    print("...................", tokenization.processed_data)
    vector_db.post_data(tokenization.processed_data)

@app.route('/token_occurrences/')
def fetch_unique_tokens():
    return token_occurrences_controller(request)
@app.route('/vector-db-details/')
def fetch_vector_db_info():
    return fetch_vector_db_info_controller(request)
