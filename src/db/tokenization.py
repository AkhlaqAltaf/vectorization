import pandas as pd
import spacy
class Tokenization:
    def __init__(self,file_path="../data_files/input/p4.csv"):
        self.file_path = file_path
        self.load_df_nlp()
        self.process_file_data()


    def load_df_nlp(self):
        self.nlp = spacy.load("en_core_web_sm")
        try:
            self.df = pd.read_csv(self.file_path, delimiter="^", header=None)
        except pd.errors.ParserError as e:
            print(f"Error reading the file: {e}")
            raise Exception

    # Function to combine entity tokens
    def combine_entity_tokens(self,doc):
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        # Create a list to store combined tokens
        combined_tokens = []
        i = 0
        while i < len(doc):
            token = doc[i]

            # Check if token is part of an entity
            is_entity = False
            for ent in doc.ents:
                if token.idx >= ent.start_char and token.idx < ent.end_char:
                    combined_tokens.append(ent.text)  # Add the entire entity as a token
                    i += len(ent)  # Skip over tokens that belong to the entity
                    is_entity = True
                    break

            if not is_entity:
                if not token.is_stop and not token.is_punct:
                    combined_tokens.append(token.text)  # Add individual non-entity tokens
                i += 1

        return combined_tokens, entities


    def process_file_data(self):
        df = self.df
        nlp = self.nlp
        # Process each row
        for index, row in df.iterrows():
            text = f"{row[2]} {row[3]}"
            doc = nlp(text)

            # Get combined tokens and entities
            combined_tokens, entities = self.combine_entity_tokens(doc)

            print(f"Row {index} Entities:", entities)
            print(f"Row {index} Unique Tokens:", combined_tokens)

        # Optionally save the unique entities and tokens back to a CSV file
        output_file = "./data_files/processed_data.csv"
        df['entities'] = df.apply(lambda row: [(ent.text, ent.label_) for ent in nlp(f"{row[2]} {row[3]}").ents], axis=1)
        df['tokens'] = df.apply(lambda row: self.combine_entity_tokens(nlp(f"{row[2]} {row[3]}"))[0], axis=1)

        # Save to CSV
        self.processed_data = df
        df.to_csv(output_file, index=False)
        print(f"Processed data with unique tokens saved to {output_file}")
        return self.processed_data
