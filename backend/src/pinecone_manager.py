from pinecone import Pinecone, ServerlessSpec
from langchain_huggingface import HuggingFaceEmbeddings
from typing import Dict, List
import os

class PineconeManager:
    def __init__(self):
        self.pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
        self.index_name = "accessibility-index"
        self.embeddings = HuggingFaceEmbeddings(
            model_name="BAAI/bge-base-en",
            model_kwargs={'device': 'cpu'}
        )
        
        self._init_index()
        
    def _init_index(self):
        if self.index_name not in self.pc.list_indexes().names():
            self.pc.create_index(
                name=self.index_name,
                dimension=768,
                metric='cosine',
                spec=ServerlessSpec(
                    cloud='aws',
                    region='us-east-1'
                )
            )
        self.index = self.pc.Index(self.index_name)

    def add_documents(self, documents: List[Dict]):
        vectors = []
        for i, doc in enumerate(documents):
            embedding = self.embeddings.embed_query(doc['content'])
            vectors.append({
                'id': f"doc_{i}",
                'values': embedding,
                'metadata': {
                    'content': doc['content'],
                    'title': doc.get('title', ''),
                    'category': doc.get('category', ''),
                    'source': doc.get('source', ''),
                    'source_url': doc.get('source_url', ''),
                    'retrieved_date': doc.get('retrieved_date', '')
                }
            })
        
        # Upsert in batches
        batch_size = 100
        for i in range(0, len(vectors), batch_size):
            batch = vectors[i:i + batch_size]
            self.index.upsert(vectors=batch)

    def search(self, query: str, category: str = None, top_k: int = 3):
        query_embedding = self.embeddings.embed_query(query)
        
        filter_dict = {"category": {"$eq": category}} if category else None
        
        results = self.index.query(
            vector=query_embedding,
            top_k=top_k,
            filter=filter_dict,
            include_metadata=True
        )
        
        return results

    def delete_all_vectors(self):
        self.index.delete(deleteAll=True)
        print("Deleted all vectors from the index")