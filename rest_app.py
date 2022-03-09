from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from db import db

from resources.user import User, UserLoggin, UserRegister
from resources.item import Item, Items
from resources.store import Store, Stores

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  ## Turns off Flask SQLAlchemy tracker; SQLAlchemy main library has it's own tracker and is better.
app.config['JWT_SECRET_Key'] = 'jose'
app.secret_key = 'jose'

api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWTManager(app)  ## Link up with the app

api.add_resource(Items, '/items')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(UserLoggin, '/login')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/<string:username>/remove')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(Stores, '/stores')

text = ('<p>Hello World! This is my Udemy REST API course project.</p>'
'/stores -- to list all the stores')

@app.route('/')
def index():
    return text

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=8888, debug=True)