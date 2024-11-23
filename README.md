# Access-Ed-Assistant


An intelligent chatbot that assists faculty in creating inclusive educational environments. Provides real-time guidance on accessibility accommodations, course material adaptation, and inclusive teaching strategies to support students with diverse learning needs.

accessibility_bot/
│
├── data/                    # Storing accessibility documents here
│   └── documents.txt
│
├── src/
│   ├── __init__.py
│   ├── document_processor.py    # Document processing logic
│   ├── embeddings_manager.py    # Embeddings and vector store logic
│   ├── chat_interface.py        # Gradio interface
│   └── main.py                  # Main application file
|
├── .env                     # Environment variables
└── requirements.txt         # Project dependencies

commands:
source accessibility_bot_env/bin/activate
pip install -r requirements.txt
cd src
python main.py


