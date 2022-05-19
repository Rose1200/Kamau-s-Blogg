import requests
from .auth.quotes import Quotes
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv('API_URL')

def get_quotes():
    response = requests.get(API_URL).json()

    return response