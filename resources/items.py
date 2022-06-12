from flask import request
from flask_jwt import jwt_required
from flask_restful import Resource

from models.item import ItemModel


class Item(Resource):
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': f"Item '{name}' doesn't exist"}, 404

    def post(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return {'message': f"Item '{name}' already exists"}, 400

        data = request.get_json()
        item = ItemModel(name, data['price'], data['store_id'])

        try:
            item.save_to_db()
        except:
            return {'message': f"Error occurred inserting '{item.name}'."}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': f"Item '{name}' deleted successfully"}
        return {'message': f"Could not find '{name}' to delete"}

    def put(self, name):
        data = request.get_json()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']

        item.save_to_db()
        return item.json()


class Items(Resource):

    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}


'''class Item(Resource):
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': f"Item '{name}' doesn't exist"}, 404

    def post(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return {'message': f"Item '{name}' already exists"}, 400

        data = request.get_json()
        item = ItemModel(name, data['price'])

        try:
            item.insert()
        except:
            return {'message': f"Error occurred inserting '{item.name}'."}, 500

        return item.json(), 201

    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'DELETE FROM items WHERE name=?'
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()
        return {'message': f"Item '{name}' deleted successfully"}

    def put(self, name):
        data = request.get_json()
        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name, data['price'])

        if item is None:
            updated_item.insert()
        else:
            updated_item.update()
        return updated_item.json()


class Items(Resource):

    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'SELECT * FROM items'
        response = cursor.execute(query)

        items = []
        for row in response:
            items.append({'name': row[0], 'price': row[1]})
        connection.close()
        return {'items': items}
'''
