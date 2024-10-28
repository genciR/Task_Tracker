import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:genci1@localhost:5432/task_tracker_db')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False


