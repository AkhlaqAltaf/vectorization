
import ast
import csv

from sqlalchemy.exc import IntegrityError

from src.sql_db.models.token_models import MetaData, Token, Entity, TokenMetaData, Word, WordMetaData, Phrase, \
    PhraseMetaData, Sentence, SentenceMetaData, Paragraph, ParagraphMetaData


def create_all_one_time(db):
    db.create_all()


class PopulateData:
    def __init__(self, db):
        self.db = db
        pass

    def populate_metadata(self, row_number, full_text, topic, text_preview, question, link, page_id, token_list):
        db = self.db
        # Check if the full_text exists in the MetaData table
        metadata = MetaData.query.filter_by(full_text=full_text, ).first()
        if not metadata:
            print("NEW META DATA CREATED..")
            # If metadata doesn't exist, insert it
            metadata = MetaData(
                paragraph_number=row_number,
                full_text=full_text,
                topic=topic,
                text_preview=text_preview,
                question=question,
                link=link,
                page_id=page_id,
                row_number=row_number,
                token_count=len(token_list),
            )
            db.session.add(metadata)
            db.session.flush()
        else:
            print("SAME META DATA USED")
        return metadata

    def populate_token_metadata(self, token_list, metadata):
        db = self.db
        token_num = 0
        for token_value in token_list:
            token_num += 0
            # Check if the token already exists
            token = Token.query.filter_by(token_value=token_value).first()

            if not token:
                print("NEW TOKEN CREATED", token_value)
                # If token doesn't exist, insert it
                token = Token(token_value=token_value)
                db.session.add(token)
                db.session.flush()  # Flush to get the token.id for TokenMetaData
            else:
                print("SAME TOKEN...", token)
            token_metadata = TokenMetaData.query.filter_by(token_id=token.id, metadata_id=metadata.id,
                                                           char_start_pos=token_num).first()
            if not token_metadata:
                print("NEW META DATA CREATED")
                # If the combination doesn't exist, insert it
                token_metadata = TokenMetaData(
                    token_id=token.id,
                    metadata_id=metadata.id,
                    char_start_pos=token_num
                )
                db.session.add(token_metadata)
            else:
                print("META DATA EXIST")
        # Commit after processing each row
        db.session.commit()

    def populate_word_metadata(self, word_list, metadata):
        db = self.db
        word_num = 0
        for word_value in word_list:
            word_num += 1
            # Check if the word already exists
            word = Word.query.filter_by(word_value=word_value).first()

            if not word:
                print("NEW WORD CREATED", word_value)
                # If word doesn't exist, insert it
                word = Word(word_value=word_value)
                db.session.add(word)
                db.session.flush()  # Flush to get the word.id for WordMetaData
            else:
                print("SAME WORD...", word)

            word_metadata = WordMetaData.query.filter_by(word_id=word.id, metadata_id=metadata.id,
                                                         char_start_pos=word_num).first()

            if not word_metadata:
                # If the combination doesn't exist, insert it
                word_metadata = WordMetaData(word_id=word.id, metadata_id=metadata.id, char_start_pos=word_num)
                db.session.add(word_metadata)

        # Commit after processing each row
        db.session.commit()

    def populate_phrase_metadata(self, phrase_list, metadata):
        db = self.db
        phrase_num = 0
        for phrase_value in phrase_list:
            phrase_num += 1
            # Check if the phrase already exists
            phrase = Phrase.query.filter_by(phrase_value=phrase_value).first()

            if not phrase:
                print("NEW PHRASE CREATED", phrase_value)
                # If phrase doesn't exist, insert it
                phrase = Phrase(phrase_value=phrase_value)
                db.session.add(phrase)
                db.session.flush()  # Flush to get the phrase.id for PhraseMetaData
            else:
                print("SAME PHRASE...", phrase)

            phrase_metadata = PhraseMetaData.query.filter_by(phrase_id=phrase.id, metadata_id=metadata.id,
                                                             char_start_pos=phrase_num).first()

            if not phrase_metadata:
                # If the combination doesn't exist, insert it
                phrase_metadata = PhraseMetaData(phrase_id=phrase.id, metadata_id=metadata.id,
                                                 char_start_pos=phrase_num)
                db.session.add(phrase_metadata)

        # Commit after processing each row
        db.session.commit()

    def populate_sentence_metadata(self, sentence_list, metadata):
        db = self.db
        sentence_num = 0
        for sentence_value in sentence_list:
            sentence_num += 1
            # Check if the sentence already exists
            sentence = Sentence.query.filter_by(sentence_value=sentence_value).first()

            if not sentence:
                print("NEW SENTENCE CREATED", sentence_value)
                # If sentence doesn't exist, insert it
                sentence = Sentence(sentence_value=sentence_value)
                db.session.add(sentence)
                db.session.flush()  # Flush to get the sentence.id for SentenceMetaData
            else:
                print("SAME SENTENCE...", sentence)

            sentence_metadata = SentenceMetaData.query.filter_by(sentence_id=sentence.id, metadata_id=metadata.id,
                                                                 char_start_pos=sentence_num).first()

            if not sentence_metadata:
                # If the combination doesn't exist, insert it
                sentence_metadata = SentenceMetaData(sentence_id=sentence.id, metadata_id=metadata.id,
                                                     char_start_pos=sentence_num)
                db.session.add(sentence_metadata)

        # Commit after processing each row
        db.session.commit()

    def populate_paragraph_metadata(self, paragraph_list, metadata):
        db = self.db
        paragraph_num = 0
        for paragraph_value in paragraph_list:
            paragraph_num += 1
            # Check if the paragraph already exists
            paragraph = Paragraph.query.filter_by(paragraph_value=paragraph_value).first()

            if not paragraph:
                print("NEW PARAGRAPH CREATED", paragraph_value)
                # If paragraph doesn't exist, insert it
                paragraph = Paragraph(paragraph_value=paragraph_value)
                db.session.add(paragraph)
                db.session.flush()  # Flush to get the paragraph.id for ParagraphMetaData
            else:
                print("SAME PARAGRAPH...", paragraph)

            paragraph_metadata = ParagraphMetaData.query.filter_by(paragraph_id=paragraph.id, metadata_id=metadata.id,
                                                                   char_start_pos=paragraph_num).first()

            if not paragraph_metadata:
                # If the combination doesn't exist, insert it
                paragraph_metadata = ParagraphMetaData(paragraph_id=paragraph.id, metadata_id=metadata.id,
                                                       char_start_pos=paragraph_num)
                db.session.add(paragraph_metadata)

        # Commit after processing each row
        db.session.commit()

    def populate_data(self, input_file='./data_files/processed_data2.csv'):
        # Read data from CSV file

        db = self.db
        with open(input_file, 'r', encoding='utf-8') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            row_number = 0
            for row in csv_reader:
                row_number += 1
                page_id = row['0']
                link = row['1']
                topic = row['2']
                full_text = row['3']
                text_preview = row['5'][:20] + "..."  # Truncate text for preview
                question = row['6']
                entities_list = row['entities']  # Assuming 'entities' is a list of tuples
                token_list = row['tokens']
                token_list = ast.literal_eval(token_list)

                paragraph_list = row['paragraphs']
                paragraph_list = ast.literal_eval(paragraph_list)

                word_list = row['words']
                word_list = ast.literal_eval(word_list)
                sentence_list = row['sentences']

                sentence_list = ast.literal_eval(sentence_list)

                phrase_list = row['phrases']
                phrase_list = ast.literal_eval(phrase_list)
                try:
                    if full_text:
                        metadata = self.populate_metadata(row_number, full_text, topic, text_preview, question, link,
                                                          page_id, token_list)
                        self.populate_token_metadata(token_list,metadata)
                        self.populate_word_metadata(word_list,metadata)
                        self.populate_phrase_metadata(phrase_list,metadata)
                        self.populate_paragraph_metadata(paragraph_list,metadata)
                        self.populate_sentence_metadata(sentence_list,metadata)

                except IntegrityError as e:
                    db.session.rollback()  # Rollback in case of error
                    print(f"IntegrityError occurred: {e}")
                except Exception as e:
                    db.session.rollback()
                    print(f"An error occurred: {e}")

