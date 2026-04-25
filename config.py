import os

class Config:
    SECRET_KEY = "secret-key"
    DATABASE = os.path.join(os.getcwd(), "database.db")