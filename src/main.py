from document_processor import DocumentProcessor
from pinecone_manager import PineconeManager
from rag_handler import RAGHandler
import gradio as gr
from dotenv import load_dotenv
import os

class AccessibilityBot:
    def __init__(self):
        load_dotenv()
        self.doc_processor = DocumentProcessor()
        self.pinecone_manager = PineconeManager()
        self.rag_handler = RAGHandler()
    
    def process_documents(self):
        documents = self.doc_processor.process_documents()
        self.pinecone_manager.add_documents(documents)
        return len(documents)
    
    def get_answer(self, query: str, category: str = None) -> str:
        results = self.pinecone_manager.search(query, category=category)
        response = self.rag_handler.generate_response(
            query=query,
            retrieved_docs=results.matches,
            category=category
        )
        return response

    def create_interface(self):
        categories = ["assistive_technology", "blindness", "deafness", None]
        examples = [
            ["What assistive technologies are available?", "assistive_technology"],
            ["What challenges do blind students face in college?", "blindness"],
            ["How can I make my course materials accessible?", None]
        ]
        
        return gr.Interface(
            fn=self.get_answer,
            inputs=[
                gr.Textbox(label="Ask a question about accessibility:"),
                gr.Dropdown(
                    choices=categories, 
                    label="Category (optional)", 
                    value=None
                )
            ],
            outputs=gr.Textbox(label="Answer"),
            title="Accessibility Education Assistant",
            description="Ask questions about making education accessible for visually impaired students",
            examples=examples,
            theme=gr.themes.Soft()
        )

def main():
    print("Initializing Accessibility Education Assistant...")
    bot = AccessibilityBot()
    print("Processing documents...")
    num_chunks = bot.process_documents()
    print(f"Processed {num_chunks} document chunks")
    print("Starting interface...")
    interface = bot.create_interface()
    interface.launch(
       share=True,
       server_name="0.0.0.0",
       server_port=7860
   )


if __name__ == "__main__":
    main()