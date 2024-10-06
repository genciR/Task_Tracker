from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config('config')

db = SQLAlchemy(app)
migrate=Migrate(app,db)

from routes import init_routes

init_routes(app)

if __name__=='__main__':
    app.run(debug=True)