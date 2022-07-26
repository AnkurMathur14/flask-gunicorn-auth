import jwt
from functools import wraps
from flask import current_app, request
from six.moves import http_client
from models.users import UserManager
        
        
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized"
            }, http_client.UNAUTHORIZED
        try:
            data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            # Get username from decoded token
            # Check if this user exists in the system
            user = UserManager().get_by_id(data["_id"])
            if not user:
                return {
                "message": "Invalid Authentication token!",
                "data": None,
                "error": "Unauthorized"
            }, http_client.UNAUTHORIZED
            # if not current_user["active"]:
                # abort(403)
        except Exception as e:
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(e)
            },  http_client.INTERNAL_SERVER_ERROR

        return f(*args, **kwargs)

    return decorated
    