from flask import render_template, jsonify

from src.sql_db.models.token_models import TokenMetaData, MetaData, Token
from src.vector_db.vectordb import VectorDb
from src.views import db  # SQLAlchemy session


def home_page_controller(request):
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

        # Vector DB processing (as per your original code)
        vector_db = VectorDb()
        results = vector_db.get_data(query_texts=input_text, return_tokens_limit=token)

        count = 0
        for result in results:
            document = result.get('documents')  # This is your token_value
            distance = result.get('distances', 1)

            # Query MetaData and TokenMetaData from the database using the token_value (document)
            metadata_query = (
                db.session.query(MetaData, TokenMetaData)
                .join(TokenMetaData, MetaData.id == TokenMetaData.metadata_id)
                .join(Token, TokenMetaData.token_id == Token.id)
                .filter(Token.token_value == document)
                .first()
            )

            if metadata_query:
                metadata, token_meta = metadata_query
                full_text = metadata.full_text or "No text available"
                char_start_pos = token_meta.char_start_pos or 0  # Retrieved from TokenMetaData
                paragraph_number = metadata.paragraph_number or 0  # Also from TokenMetaData
                row_number = metadata.row_number or 0
            else:
                full_text = "No text available"
                char_start_pos = 0
                paragraph_number = 0
                row_number = 0

            count += 1

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

        # Return JSON response for AJAX requests
        return jsonify({
            'response_message': response_message,
            'load_info_data': load_info_data,
            'reached_request_time': reached_request_time,
            'completion_info': completion_info,
            'input_text': input_text,
            'token': token
        })

    # For normal requests, render the template
    return render_template('index.html', response_message=response_message,
                           load_info_data=load_info_data,
                           reached_request_time=reached_request_time,
                           completion_info=completion_info,
                           submission_time=submission_time,
                           input_text=input_text,
                           token=token)
