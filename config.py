import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    AGIDESK_API_KEY = os.environ.get('AGIDESK_API_KEY')
    AGIDESK_BASE_URL = os.environ.get('AGIDESK_BASE_URL')