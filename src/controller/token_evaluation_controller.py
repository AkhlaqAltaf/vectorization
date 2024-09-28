import csv

from flask import render_template
from flask import jsonify

from src.db.vectordb import VectorDb


# Define the function to count paragraphs in the text
def count_paragraphs(text):
    # Assuming paragraphs are separated by double newline or some delimiter
    paragraphs = text.split('\n\n')
    return len(paragraphs), paragraphs


def token_evaluation_controller(request):
    data = []
    unique_tokens_set = set()  # To store unique tokens

    # Read data from CSV file
    with open('./data_files/processed_data.csv', 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for i, row in enumerate(csv_reader):
            row_number = i + 1
            text_preview = row['2'][:20] + "..."  # First 20 characters with ellipsis
            full_text = row['3']  # Full text to extract paragraph count
            token_list = eval(row['tokens'])  # Convert string representation to list
            token_count = len(token_list)  # Count of tokens
            paragraph_count, paragraphs = count_paragraphs(full_text)  # Count paragraphs
            unique_tokens_set.update(token_list)  # Add tokens to the set

            # Add to data list
            data.append({
                "row": row_number,
                "text_preview": text_preview,
                "token_count": token_count,
                "paragraph_count": paragraph_count,
                "tokens": sorted(token_list),  # Sorting tokens alphabetically
                "full_text": full_text,  # Full text to be displayed in popup
                "paragraphs": paragraphs,  # Paragraphs for the popup
                "entities": eval(row['entities']),  # Convert string to list of tuples
                "link": row['1']  # Link from column 1
            })
    unique_tokens_count = len(unique_tokens_set)

    return render_template('token_evaluation.html', data=data,unique_tokens=unique_tokens_count)




def fetch_vector_db_info_controller(request):
    vectordb = VectorDb()
    print(vectordb.get_db_info())
    return jsonify(vectordb.get_db_info())


def token_occurrences_controller(request):
    """Read the processed CSV file and return unique tokens with their occurrence counts."""
    token_count_dict = {}

    # Read data from CSV file
    with open('./data_files/processed_data.csv', 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            token_list = eval(row['tokens'])  # Convert string representation to list
            for token in token_list:
                if token in token_count_dict:
                    token_count_dict[token] += 1
                else:
                    token_count_dict[token] = 1

    # Convert the dictionary to a list of dictionaries
    token_occurrences_list = [{"token": token, "count": count} for token, count in token_count_dict.items()]

    return jsonify(token_occurrences_list)


