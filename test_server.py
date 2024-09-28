from datetime import timezone, datetime
import requests
from flask import Flask, render_template, request, jsonify

from src.tokenization import Tokenization
from src.vectordb import VectorDb

app = Flask(__name__)

# ChatGPT API settings
CHATGPT_API_URL = "https://api.openai.com/v1/chat/completions"
CHATGPT_API_KEY = "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"


@app.route('/', methods=['GET', 'POST'])
def index():
    response_message = []
    load_info_data = []
    submission_time = None
    completion_info = None
    reached_request_time = None
    input_text = "Common"
    token = 10
    gpt_response = ""

    if request.method == 'POST':
        print("REQUEST HIT....", request.form)

        input_text = request.form.get('inputText')
        token = int(request.form.get('token'))  # Ensure token is an integer

        # Calculate time differences in milliseconds
        vector_db = VectorDb()

        results = vector_db.get_data(query_texts=input_text, return_tokens_limit=token)
        count = 0
        for result in results:
            document = result.get('documents')
            distance = result.get('distances', 1)
            metadata = result.get('metadata', {})
            count += 1
            full_text = metadata.get('full_text', "No text available")
            char_start_pos = metadata.get('char_start_pos', 0)
            paragraph_number = metadata.get('paragraph_number', 0)
            row_number = metadata.get('row', 0)

            response_message.append({
                'text_item': document,
                'similarity': (100 - distance) if distance != 0 else 100,
                'page_id': count,
                'row_number': row_number,
                'paragraph': paragraph_number + 1,
                'char_start_pos': char_start_pos,
                'full_text': full_text
            })

            load_info_data.append({
                'text': document,
                'instances': f"Row {len(load_info_data) + 1}, Par {paragraph_number}, Pos {char_start_pos}"
            })


        # If it's an AJAX request, return JSON instead of rendering the template

        return jsonify({
            'response_message': response_message,
            'load_info_data': load_info_data,
            'reached_request_time': reached_request_time,
            'completion_info': completion_info,
            'input_text': input_text,
            'token': token
        })
    # If it's a normal request, render the full template
    return render_template('index.html', response_message=response_message,
                           load_info_data=load_info_data,
                           reached_request_time=reached_request_time,
                           completion_info=completion_info,
                           submission_time=submission_time,
                           input_text=input_text,
                           token=token)

@app.route('/submit-ai-command', methods=['POST'])
def ai_command():
    # Get the prompt from the request
    data = request.json
    prompt = data.get('prompt', '')

    # Check if prompt is not empty
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    # Call the ChatGPT API with the prompt
    try:
        response_text = call_chatgpt(prompt)
        return jsonify({"response": response_text}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def call_chatgpt(prompt):
    headers = {
        "Authorization": f"Bearer {CHATGPT_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4",
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(CHATGPT_API_URL, headers=headers, json=data)
    response_data = response.json()
    print(response_data)

    return response_data.get('choices')[0]['message']['content'] if 'choices' in response_data else "Error getting response"



def test_vect_post():
    tokenization = Tokenization(file_path="./data_files/input/p4.csv")

    vector_db = VectorDb()
    print("...................",tokenization.processed_data)
    vector_db.post_data(tokenization.processed_data)
