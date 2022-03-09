from flask import request
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token
from models.user import UserModel


class User(Resource):
    def delete(self, username):
        user = UserModel.find_by_username(username)

        if user:
            user.delete_from_db()
            return {'message':'User deleted successfully.'}
        else:
            return {'message': 'User does not exists in the database.'}


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help='This field cannot be blank.'
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help='This field cannot be blank.'
    )

    @classmethod
    def post(cls):
        data = cls.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'The username is already exists.'}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {'message': 'User registered successfully.'}


class UserLoggin(Resource):
    ## Do exactly the JWT authentication function did
    def post(self):
        # Get data from parser
        # find user in db
        # check password
        # create access token
        # create refresh token
        # return them

        data = request.get_json()
        user = UserModel.find_by_username(data['username'])
        if user and user.password == data['password']:
            # Identity is what the 'identity()' function used to do
            access_token = create_access_token(identity=1, fresh=True)
            refresh_token = create_refresh_token(1)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200

        return {'message': 'Invalid credentials'}, 401
