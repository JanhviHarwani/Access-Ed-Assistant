# main.py
from document_processor import DocumentProcessor
from pinecone_manager import PineconeManager
from rag_handler import RAGHandler
import gradio as gr
from dotenv import load_dotenv
import os
from typing import List, Dict

class ConversationalAccessibilityBot:
    def __init__(self):
        load_dotenv()
        self.doc_processor = DocumentProcessor()
        self.pinecone_manager = PineconeManager()
        self.rag_handler = RAGHandler()
        
    def process_documents(self):
        documents = self.doc_processor.process_documents()
        self.pinecone_manager.add_documents(documents)
        return len(documents)
    
    def get_response(self, message: str, history: List[List[str]]) -> str:
        # Convert history to a format that includes all previous context
        conversation_context = self._format_history(history)
        
        # Get response using RAG
        results = self.pinecone_manager.search(message)
        response = self.rag_handler.generate_response(
            query=message,
            retrieved_docs=results.matches,
            conversation_history=conversation_context
        )
        return response
    
    def _format_history(self, history: List[List[str]]) -> str:
        formatted_history = []
        for human, assistant in history:
            formatted_history.append(f"Human: {human}")
            formatted_history.append(f"Assistant: {assistant}")
        return "\n".join(formatted_history)

    def create_chat_interface(self):
        chat_interface = gr.ChatInterface(
            fn=self.get_response,
            title="Accessibility Education Assistant",
            description="Have a conversation about making education accessible for visually impaired students",
            examples=[
                ["What assistive technologies are available for visually impaired students?"],
                ["How can I make my online course materials more accessible?"],
                ["What are some best practices for teaching blind students?"]
            ],
            theme=gr.themes.Soft()
        )
        return chat_interface

def main():
    print("Initializing Conversational Accessibility Assistant...")
    bot = ConversationalAccessibilityBot()
    print("Processing documents...")
    num_chunks = bot.process_documents()
    print(f"Processed {num_chunks} document chunks")
    print("Starting chat interface...")
    chat_interface = bot.create_chat_interface()
    chat_interface.launch(
        share=True,
        server_name="0.0.0.0",
        server_port=7860
    )

if __name__ == "__main__":
    main()