import os

from src.sql_db.models.token_models import MetaData, Entity


# Utility to count paragraphs
def count_paragraphs(text):
    paragraphs = text.split('\n\n')
    return len(paragraphs), paragraphs


# Generalized method to fetch data for a specific model
def fetch_data_for_model(model, model_meta_association, model_value_field, id_name):
    data = []
    unique_values_set = set()

    # Fetch all records from the Metadata table
    records = MetaData.query.all()

    for i, record in enumerate(records):
        row_number = i + 1
        text_preview = record.full_text[:20] + "..."  # First 20 characters with ellipsis
        full_text = record.full_text  # Full text to extract paragraph count

        # Fetch all values (tokens, phrases, sentences, paragraphs) related to this metadata
        meta_associations_list = model_meta_association.query.filter_by(metadata_id=record.id).all()

        # Use the dynamic id_name to retrieve the appropriate id (e.g., word_id, phrase_id)
        value_list = [model.query.get(getattr(meta_association, id_name)) for meta_association in
                      meta_associations_list]

        value_count = len(value_list)  # Count of the values (tokens, phrases, etc.)
        paragraph_count, paragraphs = count_paragraphs(full_text)  # Count paragraphs
        unique_values_set.update([getattr(value, model_value_field) for value in value_list])  # Add values to the set

        values = sorted([getattr(value, model_value_field) for value in value_list])  # Sorting alphabetically

        # Add to data list
        data.append({
            "row": row_number,
            "text_preview": text_preview,
            "token_count": value_count,  # Generalized count
            "paragraph_count": paragraph_count,
            "tokens": values,  # Generalized values (tokens/phrases)
            "full_text": full_text,  # Full text to be displayed in popup
            "paragraphs": paragraphs,  # Paragraphs for the popup
            "entities": record.entities,  # Assuming you have an `entities` field in your table
            "link": record.link  # Link from the record
        })

    unique_values_count = len(unique_values_set)
    return data, unique_values_count


# Example usage for different models (Word, Phrase, Sentence, Paragraph)
def fetch_tokens():
    from src.sql_db.models.token_models import Token, TokenMetaData
    return fetch_data_for_model(Token, TokenMetaData, 'token_value', 'token_id')


def fetch_phrases():
    from src.sql_db.models.token_models import Phrase, PhraseMetaData
    return fetch_data_for_model(Phrase, PhraseMetaData, 'phrase_value', 'phrase_id')


def fetch_sentences():
    from src.sql_db.models.token_models import Sentence, SentenceMetaData
    return fetch_data_for_model(Sentence, SentenceMetaData, 'sentence_value', 'sentence_id')


def fetch_paragraphs():
    from src.sql_db.models.token_models import Paragraph, ParagraphMetaData
    return fetch_data_for_model(Paragraph, ParagraphMetaData, 'paragraph_value', 'paragraph_id')

def fetch_words():
    from src.sql_db.models.token_models import Word, WordMetaData
    return fetch_data_for_model(Word, WordMetaData, 'word_value', 'word_id')

# Fetch database info (unchanged)
def get_sql_db_info():
    """Fetch number of records and size on disk."""
    from src.sql_db.models.token_models import TokenMetaData
    record_count = TokenMetaData.query.count()

    # Path to the SQLite database file
    file = '../database.db'
    db_file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), file)

    # Get the size of the database file
    db_size = os.path.getsize(db_file_path)

    return {
        "record_count": record_count,
        "db_size": db_size
    }


