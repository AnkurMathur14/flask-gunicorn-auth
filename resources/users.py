import json
import flask_restful
from flask import request, jsonify
from six.moves import http_client
from werkzeug.security import generate_password_hash, check_password_hash

from utilities.validator import validate_user
from utilities.utils import save_users, get_users
from utilities.auth_middleware import token_required

# Resources
class UserList(flask_restful.Resource):
    @token_required
    def get(self):
        """
        Method to get all users.
        """
        users = get_users()
        if not users:
            return {
                "message": "No user exists",
                "data": None,
                "error": "Not found"
            }, http_client.NOT_FOUND
            
        return {
                "message": "Successfully fetched user details",
                "data": users
            }, http_client.OK

    def post(self):
        """
        Method to create a new user.
        """
        input_data = request.get_data().decode('utf-8')
        if not input_data:
            return {
                "message": "Please provide user details",
                "data": None,
                "error": "Bad request"
            }, http_client.BAD_REQUEST
        
        data = json.loads(input_data)
        ret, msg = validate_user(**data)
        if not ret:
            return {
                "message": "Invalid data",
                "data": None,
                "error": msg
            }, http_client.BAD_REQUEST
            
        users = get_users()
        for user in users:
            if user.get("username") == data.get("username"):
                return {
                    "message": "User already exists",
                    "data": None,
                    "error": "Conflict"
                }, http_client.BAD_REQUEST
                
        data["password"] = generate_password_hash(data.get("password"))
        users.append(data)
        save_users(users)
        return {
                "message": "Successfully created new user",
                "data": data
            }, http_client.CREATED


class User(flask_restful.Resource):
    @token_required
    def get(self, user_name):
        """
        Method to get a particular user.
        """
        users = get_users()
        for user in users:
            if user.get("username") == user_name:
                return {
                    "message": "Successfully fetched user details",
                    "data": user
                }, http_client.OK
        return {
                "message": "User does not exists",
                "data": None,
                "error": "Not found"
            }, http_client.NOT_FOUND

    @token_required
    def put(self, user_name):
        """
        Method to modify an exiting user.
        """
        users = get_users()
        for user in users:
            if user.get("username") == user_name:
                return {
                    "message": "Successfully fetched user details",
                    "data": user
                }, http_client.OK
        return {
                "message": "User does not exists",
                "data": None,
                "error": "Not found"
            }, http_client.NOT_FOUND
        
    @token_required
    def delete(self, user_name):
        """
        Method to delete an exiting user.
        """
        users = get_users()
        for index, user in enumerate(users):
            if user.get("username") == user_name:
                del users[index]
                save_users(users)
                return {
                    "message": "Successfully deleted the user",
                    "data": user
                }, http_client.OK
        return {
                "message": "User does not exists",
                "data": None,
                "error": "Not found"
            }, http_client.NOT_FOUND
