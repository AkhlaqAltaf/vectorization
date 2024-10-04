import os
from datetime import datetime

from flask import jsonify, send_file


def merge_files_controller(request, UPLOAD_FOLDER):
    # Ensure the upload folder exists
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    if 'file1' not in request.files or 'file2' not in request.files:
        return jsonify({'status': 'error', 'message': 'No file part in the request'})

    file_p4 = request.files['file1']
    file_p4b = request.files['file2']

    if file_p4.filename == '' or file_p4b.filename == '':
        return jsonify({'status': 'error', 'message': 'No file selected'})

    if file_p4 and file_p4b:
        # Save uploaded files with the current date and time appended to the names
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        file_path_p4 = os.path.join(UPLOAD_FOLDER, f"p4_{timestamp}_{file_p4.filename}")
        file_path_p4b = os.path.join(UPLOAD_FOLDER, f"p4b_{timestamp}_{file_p4b.filename}")
        output_file = os.path.join(UPLOAD_FOLDER, f"merged_output_{timestamp}.csv")

        # Save the uploaded files
        file_p4.save(file_path_p4)
        file_p4b.save(file_path_p4b)

        output_file_saved =merge_p4_p4b(file_path_p4, file_path_p4b, output_file)
        file_path = os.path.join(os.getcwd(), output_file_saved)

        if os.path.exists(output_file_saved):
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({'status': 'error', 'message': 'File not found'}), 500

    return jsonify({'status': 'error', 'message': 'File upload failed'})


import csv
import time
import json

def merge_p4_p4b(file_p4, file_p4b, output_file):
    # Temporary file to hold the processed p4b data
    temp_p4b_file = 'temp_p4b.csv'

    # Step 1: Replace commas with "^" in the p4b file
    with open(file_p4b, 'r') as p4b_file, open(temp_p4b_file, 'w', newline='') as temp_file:
        for line in p4b_file:
            temp_file.write(line.replace(',', '^'))

    # Step 2: Read both p4 and temp_p4b files and create output file (comma-separated)
    with open(file_p4, 'r') as f1, open(temp_p4b_file, 'r') as f2, open(output_file, 'w', newline='') as out:
        reader_p4 = csv.reader(f1, delimiter='^')
        reader_p4b = csv.reader(f2, delimiter='^')
        writer = csv.writer(out, delimiter=',')

        # Base columns before dynamic paragraph columns
        base_columns = ['p4_page_id', 'p4b_page_id', 'url', 'title', 'short_description', 'vdid', 'paragraph_list', 'full_text']

        # Create dictionaries for matching rows by pageid
        p4_dict = {row[0]: row for row in reader_p4}
        p4b_dict = {row[0]: row for row in reader_p4b}

        # Step 3: Merge rows based on pageid
        max_paragraphs = 0

        output_rows = []

        for pageid, p4_row in p4_dict.items():
            if pageid in p4b_dict:
                p4b_row = p4b_dict[pageid]

                # Dynamically process paragraphs from both p4 and p4b
                p4_paragraphs = p4_row[5:]
                p4b_paragraphs = p4b_row[1:]

                combined_paragraphs = p4_paragraphs + p4b_paragraphs
                combined_paragraphs = [para for para in combined_paragraphs if para]
                max_paragraphs = max(max_paragraphs, len(combined_paragraphs))

                paragraph_list = json.dumps(combined_paragraphs)

                full_text = ' '.join(combined_paragraphs)

                output_rows.append([pageid, pageid, p4_row[1], p4_row[2], p4_row[3], p4_row[4], paragraph_list, full_text] + combined_paragraphs)

        for i in range(1, max_paragraphs + 1):
            base_columns.append(f'paragraph_{i}')
        writer.writerow(base_columns)
        for row in output_rows:
            while len(row) < len(base_columns):
                row.append('')
            writer.writerow(row)

    # Clean up the temporary p4b file
    os.remove(temp_p4b_file)

    # Wait for the file to be saved completely
    time.sleep(2)

    return output_file

