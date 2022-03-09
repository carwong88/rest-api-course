from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required

from models.item import ItemModel


class Items(Resource):
    @jwt_required()
    def get(self):
        rows = list(map(lambda x: x.json(), ItemModel.query.all()))
        return {'items': rows}, 200


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help='This field cannot be left blank!'
    )
    parser.add_argument(
        'store_id',
        type=int,
        required=True,
        help='This field cannot be left blank!'
    )

    @jwt_required()
    def get(self, name):
        try:
            item = ItemModel.find_by_name(name)
        except Exception as error:
            return {'message': f'There is something wrong with running the query. {error}'}, 500

        if item:
            return item.json()
        return {'message': 'Item not found.'}, 404

    @jwt_required()
    def post(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return {'message': f'The item, {name}, already exists.'}, 400

        data = Item.parser.parse_args()
        new_item = ItemModel(name, data['price'], data['store_id'])

        try:
            new_item.save_to_db()
        except Exception as error:
            return {'message': f'There is a problem insert the item\n{error}.'}, 500 # Internal server error

        item = ItemModel.find_by_name(name)
        return item.json()

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}


    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item:
            item.price = data['price']
        else:
            item = ItemModel(name, data['price'], data['store_id'])

        item.save_to_db()
        return item.json()