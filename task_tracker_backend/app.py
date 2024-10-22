from flask import Flask
from extensions import db
from flask_migrate import Migrate
from flask_restful import Api
from routes import init_routes 
app = Flask(__name__)
app.config.from_object('config.Config')

db.init_app(app)
migrate = Migrate(app, db)


api = Api(app)
init_routes(api)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)