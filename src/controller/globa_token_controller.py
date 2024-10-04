from flask import render_template
from sqlalchemy import func

from src.sql_db.models.token_models import Token, TokenMetaData, Phrase, PhraseMetaData, Sentence, SentenceMetaData, \
    Paragraph, ParagraphMetaData, Word, WordMetaData
from src.views import db


def global_token_controller(request):
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
        ).join(ParagraphMetaData, Paragraph.id == ParagraphMetaData.paragraph_id) \
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

    return render_template("global_token_count.html",data =token_occurrences_list)
