import pandas as pd
import spacy

class Tokenization:
    def __init__(self, file_path,output_file):
        self.file_path = file_path
        self.load_df_nlp()
        self.out_put_file =output_file

        self.process_file_data()

    def load_df_nlp(self):
        self.nlp = spacy.load("en_core_web_sm")
        try:
            self.df = pd.read_csv(self.file_path, delimiter="^", header=None)
        except pd.errors.ParserError as e:
            print(f"Error reading the file: {e}")
            raise Exception

    # Function to combine entity tokens (Named Entity level tokenization)
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

    # Paragraph-level tokenization (Split text into paragraphs)
    def paragraph_level_tokenization(self, text):
        paragraphs = text.split("\n\n")  # Assuming paragraphs are separated by two newlines
        return paragraphs

    # Sentence-level tokenization (spaCy built-in sentence segmentation)
    def sentence_level_tokenization(self, doc):
        sentences = [sent.text for sent in doc.sents]
        return sentences

    # Word-level tokenization (spaCy word tokenization)
    def word_level_tokenization(self, doc):
        words = [token.text for token in doc if not token.is_punct and not token.is_space]
        return words

    # Phrase-level tokenization (Noun chunks or multi-word phrases)
    def phrase_level_tokenization(self, doc):
        phrases = [chunk.text for chunk in doc.noun_chunks]
        return phrases

    # Main function to process each row and apply tokenization methods
    def process_file_data(self):
        df = self.df
        nlp = self.nlp

        # Process each row
        for index, row in df.iterrows():
            text = f"{row[2]} {row[3]}"  # Assuming column 2 and 3 contain the relevant text data
            doc = nlp(text)

            # Paragraph-level tokenization
            paragraphs = self.paragraph_level_tokenization(text)
            print(f"Row {index} Paragraphs:", paragraphs)

            # Sentence-level tokenization
            sentences = self.sentence_level_tokenization(doc)
            print(f"Row {index} Sentences:", sentences)

            # Word-level tokenization
            words = self.word_level_tokenization(doc)
            print(f"Row {index} Words:", words)

            # Phrase-level tokenization
            phrases = self.phrase_level_tokenization(doc)
            print(f"Row {index} Phrases:", phrases)

            # Named Entity tokenization
            combined_tokens, entities = self.combine_entity_tokens(doc)
            print(f"Row {index} Entities:", entities)
            print(f"Row {index} Unique Tokens:", combined_tokens)

        # Optionally save the processed data back to a CSV file
        output_file = self.out_put_file
        df['entities'] = df.apply(lambda row: [(ent.text, ent.label_) for ent in nlp(f"{row[2]} {row[3]}").ents], axis=1)
        df['paragraphs'] = df.apply(lambda row: self.paragraph_level_tokenization(f"{row[2]} {row[3]}"), axis=1)
        df['sentences'] = df.apply(lambda row: self.sentence_level_tokenization(nlp(f"{row[2]} {row[3]}")), axis=1)
        df['words'] = df.apply(lambda row: self.word_level_tokenization(nlp(f"{row[2]} {row[3]}")), axis=1)
        df['phrases'] = df.apply(lambda row: self.phrase_level_tokenization(nlp(f"{row[2]} {row[3]}")), axis=1)
        df['tokens'] = df.apply(lambda row: self.combine_entity_tokens(nlp(f"{row[2]} {row[3]}"))[0], axis=1)

        # Save to CSV
        self.processed_data = df
        df.to_csv(output_file, index=False)
        print(f"Processed data saved to {output_file}")
        return self.processed_data
