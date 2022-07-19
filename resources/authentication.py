import json
import jwt
import flask_restful
from flask import current_app, request
from six.moves import http_client
from werkzeug.security import generate_password_hash, check_password_hash

from utilities.validator import validate_username_and_password
from utilities.utils import save_users, get_users

class Authentication(flask_restful.Resource):
    def post(self):
        """
        Method to login and generate JWT
        """
        input_data = request.get_data().decode('utf-8')
        if not input_data:
            return {
                "message": "Please provide user details",
                "data": None,
                "error": "Bad request"
            }, http_client.BAD_REQUEST

        data = json.loads(input_data)
        
        # validate input
        is_validated, msg = validate_username_and_password(data.get('username'), data.get('password'))
        if is_validated is not True:
            return {
                "message": 'Invalid data',
                "data": None,
                "error": msg
            }, http_client.BAD_REQUEST

        # check if user exists
        users = get_users()
        found = False
        password = None
        for user in users:
            if user.get("username") == data.get('username'):
                found = True
                password = user.get("password")
                break
               
        if not found:        
            return {
                    "message": "User does not exists",
                    "data": None,
                    "error": "Not found"
                }, http_client.NOT_FOUND

        # Validate user
        if not check_password_hash(password, data.get('password')):
            return {
                "message": "Invalid username or password",
                "data": None,
                "error": "Unauthorized"
            }, http_client.UNAUTHORIZED

        try:
            # token should expire after 24 hrs
            user["token"] = jwt.encode(
                {"username": user["username"]},
                current_app.config["SECRET_KEY"],
                algorithm="HS256"
            )
            user.pop("password")
            return {
                "message": "Successfully fetched auth token",
                "data": user
            }
        except Exception as e:
            return {
                "error": "Something went wrong",
                "message": str(e)
            }, http_client.BAD_REQUEST
