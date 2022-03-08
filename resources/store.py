from flask_restful import Resource, reqparse
from models.store import StoreModel


class Stores(Resource):
    def get(self):
        stores = StoreModel.query.all()
        return {'stores': [ each.json() for each in stores ]}


class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'This store does not exist.'}, 404

    def post(self, name):
        store = StoreModel.find_by_name(name)

        if store:
            return {'message': 'Store already existed.'}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except Exception as error:
            return {'message': f'An error occurred while creating the store.\n{error}'}, 500

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)

        if store:
            store.delete_from_db()
            return {'message': 'Store is deleted from database.'}
        else:
            return {'message': 'Store does not exits.'}



