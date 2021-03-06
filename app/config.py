import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """"""
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    


class ProdConfig(Config):
    """"""
    
class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')

config_options = {
    'prod':ProdConfig, 
    'dev':DevConfig
}    