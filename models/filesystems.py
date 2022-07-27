import bson
from utilities.database import DBManager

class FSManager:
    """Filesystem DB operations"""
    def __init__(self):
        self.collection_name = "filesystems"
        self.db_manager = DBManager(self.collection_name)

    def create(self, name="", size="", media=""):
        """Create a new filesystem"""

        # Check if already exists
        filesystem = self.db_manager.search({"name": name})
        if filesystem:
            return None

        # Create a new filesystem
        new_filesystem = self.db_manager.insert(
            [{
                "name": name,
                "size": size,
                "media": media
            }]
        )

        # Return the created filesystem
        return self.get_by_name(name)

    def get_all(self):
        """Get all filesystems"""
        return self.db_manager.search()

    def get_by_name(self, fs_name):
        """Get a filesystem by name"""
        return self.db_manager.search({"name": fs_name})

    def get_by_id(self, fs_id):
        """Get a filesystem by id"""
        # Check if given id is valid
        if not bson.ObjectId.is_valid(fs_id):
            return None

        return self.db_manager.search({"_id": bson.ObjectId(fs_id)})

    def update(self, fs_id, name=None, size=None, media=None):
        """Update a filesystem"""
        data = {}
        if name:
            data["name"] = name
        if size:
            data["size"] = size
        if media:
            data["media"] = media

        if not fs_id:
            return None

        # Check if given id is valid
        if not bson.ObjectId.is_valid(fs_id):
            return None

        # Check if fs id exists
        filesystem = self.get_by_id(fs_id)
        if not filesystem:
            return None

        # Update filesystes
        filesystem = self.db_manager.update(
            {"_id": bson.ObjectId(fs_id)},
            {
                "$set": data
            }
        )

        # Get updated details
        filesystem = self.get_by_id(fs_id)
        return filesystem

    def delete(self, fs_id):
        """Delete a filesystem by name"""

        # Check if given id is valid
        if not bson.ObjectId.is_valid(fs_id):
            return None

        filesystem = self.db_manager.delete({"_id": bson.ObjectId(fs_id)})
        if not filesystem:
            return None
        else:
            return True