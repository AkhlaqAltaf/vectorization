import pandas as pd
import spacy



class Tokenization:
    def __init__(self, file_path, output_file):
        self.file_path = file_path
        self.output_file = output_file
        self.nlp = spacy.load("en_core_web_sm")  # Load the spaCy model
        self.process_file_data()

    def combine_entity_tokens(self, doc):
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        combined_tokens = []
        i = 0
        while i < len(doc):
            token = doc[i]
            is_entity = False
            for ent in doc.ents:
                if token.idx >= ent.start_char and token.idx < ent.end_char:
                    combined_tokens.append(ent.text)
                    i += len(ent)  # Skip tokens belonging to the entity
                    is_entity = True
                    break
            if not is_entity:
                if not token.is_stop and not token.is_punct:
                    combined_tokens.append(token.text)
                i += 1
        return combined_tokens, entities

    def sentence_level_tokenization(self, doc):
        return [sent.text for sent in doc.sents]

    def word_level_tokenization(self, doc):
        return [token.text for token in doc if not token.is_punct and not token.is_space]

    def phrase_level_tokenization(self, doc):
        return [chunk.text for chunk in doc.noun_chunks]

    def process_file_data(self):
        # Load the CSV file and the relevant columns
        df = pd.read_csv(self.file_path, usecols=[
            'p4_page_id', 'title', 'url', 'short_description', 'full_text', 'paragraph_list'
        ])

        processed_rows = []

        for index, row in df.iterrows():
            doc = self.nlp(row['full_text'])

            # Tokenization and entity extraction
            sentences = self.sentence_level_tokenization(doc)
            words = self.word_level_tokenization(doc)
            phrases = self.phrase_level_tokenization(doc)
            combined_tokens, entities = self.combine_entity_tokens(doc)

            # Construct a new row with the required fields
            new_row = {
                'page_id': row['p4_page_id'],
                'title': row['title'],
                'url': row['url'],
                'short_description': row['short_description'],
                'full_text': row['full_text'],
                'paragraph_list': row['paragraph_list'],  # Already in list form
                'sentences': sentences,
                'words': words,
                'phrases': phrases,
                'entities': entities,
                'combined_tokens': combined_tokens
            }

            # Append the new row to the processed data list
            processed_rows.append(new_row)

        # Create a new DataFrame with only the required fields
        new_df = pd.DataFrame(processed_rows)

        # Save the new DataFrame to the specified output file
        new_df.to_csv(self.output_file, index=False)
        print(f"Processed data saved to {self.output_file}")

        return new_df


