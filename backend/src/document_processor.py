from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
import re
from typing import List, Dict
from pinecone_manager import PineconeManager

class DocumentProcessor:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.categories_dir = os.path.join(self.base_dir, 'data', 'categories')
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        self.pinecone_manager = PineconeManager()

    def extract_metadata(self, text: str) -> Dict:
        """Extract metadata from document text including title, source URL, and retrieval date."""
        metadata = {}
        
        # Extract title
        title_match = re.search(r'Title:\s*(.*?)\s*Source URL:', text)
        if title_match:
            metadata['title'] = title_match.group(1).strip()

        # Extract source URL
        url_match = re.search(r'Source URL:\s*(.*?)\s*Retrieved:', text)
        if url_match:
            metadata['source_url'] = url_match.group(1).strip()

        # Extract retrieval date
        date_match = re.search(r'Retrieved:\s*(.*?)\s*Content:', text)
        if date_match:
            metadata['retrieved_date'] = date_match.group(1).strip()

        return metadata

    def process_documents(self) -> List[Dict]:
        RELOAD_DOCUMENTS = os.getenv('RELOAD_DOCUMENTS', 'false').lower() == 'true'
        
        if not RELOAD_DOCUMENTS:
            print("Skipping document processing - RELOAD_DOCUMENTS is false")
            return []
        
        print("Starting document processing...")
        # Step 1: Clean up existing index
        print("Cleaning up Pinecone index...")
        self.pinecone_manager.delete_all_vectors()  
        
        # Step 2: Process new documents
        documents = []
        print(f"Found categories: {os.listdir(self.categories_dir)}")
        
        for category in os.listdir(self.categories_dir):
            category_path = os.path.join(self.categories_dir, category)
            if os.path.isdir(category_path):
                print(f"Processing category: {category}")
                num_files = len([f for f in os.listdir(category_path) if f.endswith('.txt')])
                print(f"Found {num_files} files in {category}")
                
                for filename in os.listdir(category_path):
                    if filename.endswith('.txt'):
                        filepath = os.path.join(category_path, filename)
                        loader = TextLoader(filepath, encoding='utf-8')
                        file_docs = loader.load()
                        
                        for doc in file_docs:
                            # Extract metadata before splitting
                            metadata = self.extract_metadata(doc.page_content)
                            
                            # Split the document
                            texts = self.text_splitter.split_documents([doc])
                            
                            for text in texts:
                                documents.append({
                                    'content': text.page_content,
                                    'category': category,
                                    'filename': filename,
                                    'source': filepath,
                                    'title': metadata.get('title', ''),
                                    'source_url': metadata.get('source_url', ''),
                                    'retrieved_date': metadata.get('retrieved_date', '')
                                })
        
        print(f"Processed {len(documents)} document chunks")
        return documents