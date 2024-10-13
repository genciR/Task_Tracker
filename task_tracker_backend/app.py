from flask import Flask
from extensions import db
from flask_migrate import Migrate
from flask_restful import Api

app = Flask(__name__)
app.config.from_object('config.Config')

db.init_app(app)


migrate = Migrate(app, db)


api = Api(app)


with app.app_context():
    from models import User, Task, Skill, Assignment

if __name__ == '__main__':
    app.run(debug=True)