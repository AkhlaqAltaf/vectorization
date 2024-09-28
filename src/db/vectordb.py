import os
import chromadb
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction
import spacy
import uuid
import pandas as pd
from dotenv import load_dotenv

input_file = "../../data_files/processed_data.csv"

class VectorDb:
    def __init__(self):
        load_dotenv('./.env.local')
        storage_path = os.getenv('STORAGE_PATH')
        if storage_path is None:
            raise ValueError('STORAGE_PATH environment variable is not set')

        self.nlp = spacy.load("en_core_web_sm")
        self.client = chromadb.PersistentClient(path=storage_path)



    def post_data(self,df):
        nlp = self.nlp
        # Get or create the collection in ChromaDB
        df = pd.read_csv("./data_files/processed_data.csv")
        client = self.client
        collection = client.get_or_create_collection(name="chroma")
        processed_tokens = set()
        # Loop through the data and create vectors from tokens
        for index, row in df.iterrows():
            tokens = eval(row['tokens'])
            count = 0
            for token in tokens:
                if token not in processed_tokens:
                    count += 1
                    vector = nlp(token).vector.tolist()
                    print(f"VECTOR OF {token} IS  :  {vector}")

                    collection.add(
                        documents=[token],
                        embeddings=[vector],
                        ids=f"id{uuid.uuid4()}",
                        metadatas=[{"row":row.get('0'),"char_start_pos": count, "full_text": row.get('3'), "paragraph_number": index}]
                    )
                    processed_tokens.add(token)
        return collection
        print("Vector database created and populated without duplicates.")
    def get_data(self,query_texts, return_tokens_limit):
        nlp = self.nlp
        client = self.client
        collection = client.get_collection(name="chroma")
        query = query_texts
        query_vector = nlp(query).vector.tolist()
        results = collection.query(
            query_embeddings=[query_vector],
            n_results=return_tokens_limit
        )
        results_list = []

        for n in range(len(results['ids'][0])):
            # Access the document directly as it's a list of strings
            token = results['documents'][0][n]
            distance = results['distances'][0][n]

            doc_id = results['ids'][0][n]
            metadata = results['metadatas'][0][n]  # Access the metadata

            results_list.append({
                'ids': doc_id,
                "distances": distance,
                "documents": token,
                "metadata": metadata
            })

        return results_list
