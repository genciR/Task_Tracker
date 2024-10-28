from flask import Flask
from extensions import db
from flask_migrate import Migrate
from flask_restful import Api
from routes import init_routes 


app = Flask(__name__)
app.config.from_object('config.Config')
app.config['JWT_SECRET_KEY'] = 'sdkfjhdsi3839!nkjdf4nNNNdn' 
db.init_app(app)
migrate = Migrate(app, db)

# cors.init_app(app,resources={r"/api/*":{"origins":["http//localhost"]}})
# jwt.init_app(app)
api = Api(app)
init_routes(api)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)