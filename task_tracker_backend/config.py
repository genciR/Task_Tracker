import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:genci1@localhost:5432/task_tracker_db')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_TOKEN_KEY=os.environ.get("JWT_SECRET_KEY")
    JWT_TOKEN_LOCATION=["headers"]
    JWT_TOKEN_IDENTITY_CLAIM="user_id" 

