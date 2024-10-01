from flask import render_template, jsonify
from src.vector_db.vectordb import VectorDb



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
