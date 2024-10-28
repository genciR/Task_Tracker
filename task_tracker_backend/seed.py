from app import app
from extensions import db, pwd_context
from models import User

user_data=[
    {'name': 'Alice Smith', 'email': 'alice@example.com', 'role': 'admin', 'password': 'securepassword1'},
    {'name': 'Bob Johnson', 'email': 'bob@example.com', 'role': 'user', 'password': 'securepassword2'},
    {'name': 'Charlie Brown', 'email': 'charlie@example.com', 'role': 'user', 'password': 'securepassword3'},
]

with app.app_context():
    db.create_all()
    for user_data in user_data:
        user=User(**user_data)
        db.session.add(user)

    db.session.commit()

print("Seeding completed!!")