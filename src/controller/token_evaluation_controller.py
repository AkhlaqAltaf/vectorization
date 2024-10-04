import csv

from flask import render_template
from flask import jsonify
from sqlalchemy import func

from src.sql_db.models.token_models import Phrase, Token, TokenMetaData, PhraseMetaData, Sentence, SentenceMetaData, \
    Paragraph, ParagraphMetaData, Word, WordMetaData
from src.sql_db.queries.fetch_evaluation_data import (fetch_paragraphs, get_sql_db_info ,
                                                      fetch_phrases ,
                                                      fetch_sentences ,
                                                      fetch_tokens,
                                                      fetch_words)
from src.vector_db.vectordb import VectorDb
from src.views import db


# Define the function to count paragraphs in the text
def count_paragraphs(text):
    # Assuming paragraphs are separated by double newline or some delimiter
    paragraphs = text.split('\n\n')
    return len(paragraphs), paragraphs


def token_evaluation_controller(request):
    # <td>{{ item.row }}</td> <!-- Page # (Row number) -->
    # <td>{{ item.match_context }}</td> <!-- Match Context, leave blank if no search -->
    # <td>{{ item.similarity }}%</td> <!-- Similarity percentage -->
    # <td>{{ item.text_preview[:20] }}...</td> <!-- Text preview -->
    # <td>{{ item.page_type }}</td> <!-- Page Type: URL, Title, or paragraph number -->
    # <td>{{ item.word_token_count }}</td> <!-- Word Tokens Count -->
    # <td>{{ item.phrase_token_count }}</td> <!-- Phrase Tokens Count -->
    # <td>{{ item.sentence_token_count }}</td> <!-- Sentence Tokens Count -->
    # <td>{{ item.paragraph_token_count }}</td> <!-- Paragraph Tokens Count -->
    # <td>{{ item.paragraph_count }}</td> <!-- Paragraph Count -->
    model = request.args.get('model')
    print("MODELS",model)
    tokens , unique_tokens_count=fetch_tokens()

    phrases, unique_tokens_count = fetch_phrases()
    sentences, unique_tokens_count = fetch_sentences()
    paragraphs, unique_tokens_count = fetch_paragraphs()
    words, unique_tokens_count = fetch_words()
    items = []
    for i in range(len(tokens)):

        data = {
            'row':tokens[i]['row'],
            'paragraph_count':tokens[i]['paragraph_count'],
            'text_preview':tokens[i]['text_preview'],
            'page_type':tokens[i]['topic'],
            'url':tokens[i]['link'],
            'word_token_count':words[i]['token_count'],
            'phrase_token_count':phrases[i]['token_count'],
            'sentence_token_count':sentences[i]['token_count'],
            'paragraph_token_count':paragraphs[i]['token_count'],

             }
        items.append(data)

    return render_template('main_search.html', data=items,unique_tokens=unique_tokens_count)



def fetch_vector_db_info_controller(request):
    vectordb = VectorDb()
    print("DATA WILL BE HERE ...",vectordb.get_db_info())
    return jsonify(vectordb.get_db_info())
def fetch_sql_db_info_controller(request):
    sql_info=get_sql_db_info()
    print("SQL DB INFO-------",sql_info)

    return jsonify(sql_info)
def token_occurrences_controller(request):
    """Fetch tokens and their occurrence counts from the SQL database."""
    model = request.args.get('model')
    if model =="tokens":
        token_count_data = db.session.query(
            Token.token_value,
            func.count(TokenMetaData.token_id).label('count')
        ).join(TokenMetaData, Token.id == TokenMetaData.token_id) \
            .group_by(Token.token_value).all()

    elif  model=='phrase':
        token_count_data = db.session.query(
            Phrase.phrase_value,
            func.count(PhraseMetaData.phrase_id).label('count')
        ).join(PhraseMetaData, Phrase.id == PhraseMetaData.phrase_id) \
        .group_by(Phrase.phrase_value).all()


    elif model =='sentence':
        token_count_data = db.session.query(
            Sentence.sentence_value,
            func.count(SentenceMetaData.sentence_id).label('count')
        ).join(SentenceMetaData, Sentence.id == SentenceMetaData.sentence_id) \
        .group_by(Sentence.sentence_value).all()


    elif model =='paragraph':
        token_count_data = db.session.query(
            Paragraph.paragraph_value,
            func.count(ParagraphMetaData.paragraph_id).label('count')
        ).join(ParagraphMetaData, Paragraph.id == ParagraphMetaData.phrase_id) \
        .group_by(Paragraph.paragraph_value).all()
    elif model =="word":
        token_count_data = db.session.query(
            Word.word_value,
            func.count(WordMetaData.word_id).label('count')
        ).join(WordMetaData, Word.id == WordMetaData.word_id) \
        .group_by(Word.word_value).all()

    else:
        token_count_data = db.session.query(
            Token.token_value,
            func.count(TokenMetaData.token_id).label('count')
        ).join(TokenMetaData, Token.id == TokenMetaData.token_id) \
            .group_by(Token.token_value).all()


    # Convert the query result to a list of dictionaries
    token_occurrences_list = [{"token": token, "count": count} for token, count in token_count_data]

    return jsonify(token_occurrences_list)














