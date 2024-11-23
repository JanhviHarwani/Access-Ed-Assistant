# src/document_processor.py

from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from typing import List, Dict

class DocumentProcessor:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.categories_dir = os.path.join(self.base_dir, 'data', 'categories')
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )

    def process_documents(self) -> List[Dict]:
        documents = []
        
        # Walk through category directories
        for category in os.listdir(self.categories_dir):
            category_path = os.path.join(self.categories_dir, category)
            if os.path.isdir(category_path):
                print(f"Processing category: {category}")
                for filename in os.listdir(category_path):
                    if filename.endswith('.txt'):
                        filepath = os.path.join(category_path, filename)
                        loader = TextLoader(filepath, encoding='utf-8')
                        file_docs = loader.load()
                        
                        # Split documents
                        texts = self.text_splitter.split_documents(file_docs)
                        
                        # Add metadata
                        for text in texts:
                            documents.append({
                                'content': text.page_content,
                                'category': category,
                                'filename': filename,
                                'source': filepath
                            })
        
        print(f"Processed {len(documents)} document chunks")
        return documents