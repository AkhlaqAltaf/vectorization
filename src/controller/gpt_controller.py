import requests
from flask import jsonify
from src.tokenization.tokenization import Tokenization
from src.vector_db.vectordb import VectorDb


# ChatGPT API settings
CHATGPT_API_URL = "https://api.openai.com/v1/chat/completions"
CHATGPT_API_KEY = "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"



def ai_command_controller(request):
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
