import json
import uuid
import flask_restful
from flask import request, jsonify
from six.moves import http_client

from models.users import UserManager
from utilities.validator import validate_user
from utilities.auth_middleware import token_required

# Resources
class UserList(flask_restful.Resource):
    @token_required
    def get(self):
        """
        Method to get all users.
        """
        users = UserManager().get_all()
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
            
        user = UserManager().create(**data)
        if not user:
            return {
                "message": "User already exists",
                "data": None,
                "error": "Conflict"
            }, http_client.BAD_REQUEST
        return {
                "message": "The user has been created",
                "data": user
            }, http_client.CREATED


class User(flask_restful.Resource):
    @token_required
    def get(self, user_id):
        """
        Method to get a particular user.
        """
        user = UserManager().get_by_id(user_id)
        if not user:
            return {
                "message": "User does not exists",
                "data": None,
                "error": "Not found"
            }, http_client.NOT_FOUND

        return {
            "message": "Successfully fetched user details",
            "data": user
        }, http_client.OK


    @token_required
    def put(self, user_id):
        """
        Method to modify an exiting user.
        """
        user = UserManager().disable_account(user_id)
        if not user:
            return {
                "message": "User does not exists",
                "data": None,
                "error": "Not found"
            }, http_client.NOT_FOUND

        return {
            "message": "The user has been disabled",
            "data": user
        }, http_client.OK
        

    @token_required
    def delete(self, user_id):
        """
        Method to delete an exiting user.
        """
        user = UserManager().delete(user_id)
        if not user:
            return {
                "message": "User does not exists",
                "data": None,
                "error": "Not found"
            }, http_client.NOT_FOUND

        return {
            "message": "The user has been deleted",
            "data": user
        }, http_client.OK
