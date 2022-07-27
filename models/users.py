import bson
from werkzeug.security import generate_password_hash, check_password_hash
from utilities.database import DBManager

class UserManager:
    """User DB operations"""
    def __init__(self):
        self.collection_name = "users"
        self.db_manager = DBManager(self.collection_name)

    def create(self, username="", email="", password=""):
        """Create a new user"""

        # Check if already exists
        user = self.db_manager.search({"username": username})
        if user:
            return None

        # Create new user
        new_user = self.db_manager.insert(
            [{
                "username": username,
                "email": email,
                "password": self.encrypt_password(password),
                "active": True
            }]
        )

        # Return the created user
        return self.db_manager.search({"username": username})

    def get_all(self):
        """Get all users"""
        return self.db_manager.search()

    def get_by_name(self, user_name):
        """Get a user by name"""
        return self.db_manager.search({"username": user_name})

    def get_by_email(self, email):
        """Get a user by emain"""
        return self.db_manager.search({"email": email})

    def get_by_id(self, user_id):
        """Get a user by id"""
        # Check if given id is valid
        if not bson.ObjectId.is_valid(user_id):
            return None

        return self.db_manager.search({"_id":  bson.ObjectId(user_id)})

    def update(self, user_id, username="", email=""):
        """Update a user by ID"""
        data = {}
        if username:
            data["username"] = username
        if email:
            data["email"] = email

        # Check if given id is valid
        if not bson.ObjectId.is_valid(user_id):
            return None

        # Check if user id exists
        user = self.get_by_id(user_id)
        if not user:
            return None

        # Update the user
        users = self.db_manager.update(
            {"_id": bson.ObjectId(user_id)},
            {
                "$set": data
            }
        )

        # Get the updated user
        user = self.get_by_id(user_id)
        return user

    def delete(self, user_id):
        """Delete a user"""

        # Check if given id is valid
        if not bson.ObjectId.is_valid(user_id):
            return None

        user = self.db_manager.delete({"_id": bson.ObjectId(user_id)})
        if not user:
            return None
        else:
            return True

    def disable_account(self, user_id):
        """Disable a user account"""

        # Check if given id is valid
        if not bson.ObjectId.is_valid(user_id):
            return None

        # Check if user exists
        user = self.db_manager.search({"_id": bson.ObjectId(user_id)})
        if not user:
            return None
        user = self.db_manager.update(
            {"_id": user_id},
            {"$set": {"active": False}}
        )
        user = self.get_by_id(user_id)
        return user

    def encrypt_password(self, password):
        """Encrypt password"""
        return generate_password_hash(password)
