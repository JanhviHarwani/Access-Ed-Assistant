to start scraping:
cd backend
source venv/bin/activate
cd src/scraping_scripts 
python web_processor.py

start backend:
cd backend
source venv/bin/activate
pip install -r requirements.txt
cd src
python main.py

start frontend:
cd frontend
npm start