import os

from flask import Flask, current_app
from flask_jwt import JWT
from flask_restful import Api

from db import db
from resources.items import Item, Items
from resources.stores import Store, StoreList
from security import authenticate, identity
from resources.users import UserRegister


class CustomApi(Api):
    def handle_error(self, e):
        for val in current_app.error_handler_spec.values():
            for handler in val.values():
                registered_error_handlers = list(filter(lambda x: isinstance(e, x), handler.keys()))
                if len(registered_error_handlers) > 0:
                    raise e
        return super().handle_error(e)


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI", 'sqlite:///data.db')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False
api = CustomApi(app)
app.secret_key = 'jsdf'
jwt = JWT(app, authenticate, identity)


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Items, '/items')
api.add_resource(UserRegister, '/register')


if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000)

# stores = [
#     {
#         'name': 'My Store',
#         'items': [
#             {
#                 'name': 'My Item',
#                 'price': 15.99
#             }
#         ]
#     }
# ]
#
#
# @app.route('/')
# def home():
#     return render_template('index.html')
#
#
# @app.route('/store', methods=['POST'])
# def create_store():
#     request_data = request.get_json()
#     new_store = {
#         'name': request_data['name'],
#         'items': []
#     }
#     stores.append(new_store)
#     return jsonify(new_store)
#
#
# @app.route('/store/<string:name>')
# def get_store(name):
#     for store in stores:
#         if store['name'] == name:
#             return jsonify(store)
#     return jsonify({'message': 'Store not found'})
#
#
# @app.route('/store')
# def get_stores():
#     return jsonify({'stores': stores})
#
#
# @app.route('/store/<string:name>/item', methods=['POST'])
# def create_item_in_store(name):
#     request_data = request.get_json()
#     for store in stores:
#         if store['name'] == name:
#             new_item = {
#                 'name': request_data['name'],
#                 'price': request_data['price']
#             }
#             store['items'].append(new_item)
#             return jsonify(new_item)
#     return jsonify({'message': 'Store not found'})
#
#
# @app.route('/store/<string:name>/item')
# def get_item_in_store(name):
#     for store in stores:
#         if store['name'] == name:
#             return jsonify({'items': store['items']})
#     return jsonify({'message': 'Items not found'})
