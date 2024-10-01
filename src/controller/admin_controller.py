import os
from datetime import datetime

from flask import jsonify

from src.sql_db.queries.populate_data import PopulateData
from src.tokenization.tokenization import Tokenization
from src.views import db


def upload_file_controller(request,UPLOAD_FOLDER):

    if 'file' not in request.files:
        return jsonify({'status': 'error', 'message': 'No file part in the request'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'status': 'error', 'message': 'No file selected'})

    if file:
        # Save file with the current date and time appended to its name
        filename = file.filename
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename_with_timestamp = f"{timestamp}_{filename}"
        filename_with_timestamp_output = f"{timestamp}_output_{filename}"

        os.path.join(UPLOAD_FOLDER, filename_with_timestamp)
        file_path=os.path.join(UPLOAD_FOLDER, filename_with_timestamp)
        output_file_path=os.path.join(UPLOAD_FOLDER, filename_with_timestamp_output)

        file.save(file_path)
        tokenize= Tokenization(file_path=file_path,output_file=output_file_path)
        populate_data = PopulateData(db=db)
        populate_data.populate_data(tokenize.out_put_file)
        return jsonify({'status': 'success', 'message': 'File uploaded successfully', 'filename': filename_with_timestamp})

    return jsonify({'status': 'error', 'message': 'File upload failed'})