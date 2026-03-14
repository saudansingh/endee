import os
from utils.embedding import Embedder
from utils.vector_store import EndeeStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

def run_ingestion():
    embedder = Embedder()
    store = EndeeStore()
    
    # Setup collection
    store.create_collection("docs_collection", embedder.dimension)

    # Load your data (assumes .txt files in data folder)
    data_dir = "./data"
    for filename in os.listdir(data_dir):
        if filename.endswith(".txt"):
            with open(os.path.join(data_dir, filename), 'r') as f:
                text = f.read()
                
                splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
                chunks = splitter.split_text(text)
                
                vectors = embedder.encode(chunks)
                payloads = [{"text": c, "source": filename} for c in chunks]
                
                store.insert_data("docs_collection", vectors, payloads)
                print(f"Indexed {filename}")

if __name__ == "__main__":
    run_ingestion()