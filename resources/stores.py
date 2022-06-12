from flask_jwt import jwt_required
from flask_restful import Resource

from models.store import StoreModel


class Store(Resource):
    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': f"Store '{name}' doesn't exist"}, 404

    def post(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return {'message': f"Store '{name}' already exists"}, 400

        store = StoreModel(name)

        try:
            store.save_to_db()
        except:
            return {'message': f"Error occurred inserting '{store.name}'."}, 500

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {'message': f"Store '{name}' deleted successfully"}
        return {'message': f"Could not find '{name}' to delete"}


class StoreList(Resource):

    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
