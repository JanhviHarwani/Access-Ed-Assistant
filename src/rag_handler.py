# src/rag_handler.py

from openai import OpenAI
import os
from typing import List, Dict

class RAGHandler:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
    def generate_response(self, query: str, retrieved_docs: List[Dict], category: str = None) -> str:
        # Handle general chat
        if self._is_general_chat(query):
            return self._handle_general_chat(query)
            
        # Prepare context from retrieved documents
        context = self._prepare_context(retrieved_docs)
        
        # Create prompt
        prompt = self._create_prompt(query, context, category)
        
        # Get response from GPT
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert assistant helping educators make education accessible for visually impaired students. Your responses should be clear, structured, and actionable."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=250
        )
        
        return response.choices[0].message.content

    def _is_general_chat(self, query: str) -> bool:
        greetings = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']
        gratitude = ['thanks', 'thank you', 'appreciate']
        farewell = ['bye', 'goodbye', 'see you', 'farewell']
        
        query_lower = query.lower()
        return any(word in query_lower for word in greetings + gratitude + farewell)

    def _handle_general_chat(self, query: str) -> str:
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['hello', 'hi', 'hey']):
            return "Hello! I'm here to help you make education more accessible for visually impaired students. What would you like to know?"
            
        if any(word in query_lower for word in ['thanks', 'thank you']):
            return "You're welcome! Feel free to ask if you have any more questions about accessibility."
            
        if any(word in query_lower for word in ['bye', 'goodbye']):
            return "Goodbye! Don't hesitate to return if you need more assistance with accessibility matters."
            
        return "I'm here to help with your accessibility-related questions!"

    def _prepare_context(self, retrieved_docs: List[Dict]) -> str:
        context = []
        for doc in retrieved_docs:
            content = doc.metadata.get('content', '')
            source = doc.metadata.get('source', '')
            if content:
                context.append(f"Content: {content}\nSource: {source}\n")
        return "\n".join(context)

    def _create_prompt(self, query: str, context: str, category: str = None) -> str:
        category_context = f" focusing on {category}" if category else ""
        
        return f"""Based on the following context{category_context}, provide a clear and structured response to the query: "{query}"

Context:
{context}

Please structure your response with:
1. A brief introduction
2. Key points or main information
3. Specific examples or applications where relevant
4. Any important considerations or best practices
5. Remember to maintain a supportive and educational tone

Query: {query}"""