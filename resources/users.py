from flask import request
from flask_restful import Resource

from models.user import UserModel


class UserRegister(Resource):

    def post(self):
        data = request.get_json()
        if UserModel.find_by_username(data['username']):
            return {'message': f"User with username '{data['username']}' already exists"}, 409

        user = UserModel(data['username'], data['password'])
        user.save_to_db()
        return {'message': 'User created successfully.'}, 201


'''class UserRegister(Resource):

    def post(self):
        data = request.get_json()
        if UserModel.find_by_username(data['username']):
            return {'message': f"User with username '{data['username']}' already exists"}, 409

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'INSERT INTO users VALUES (NULL, ?, ?)'
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()
        return {'message': 'User created successfully.'}, 201'''
