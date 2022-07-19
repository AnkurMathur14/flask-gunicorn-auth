import json
import flask_restful
from flask import request
from six.moves import http_client

from utilities.utils import save_filesystems, get_filesystems
from utilities.auth_middleware import token_required

class FileSystemList(flask_restful.Resource):
    @token_required
    def get(self):
        """
        Method to fetch all the filesystems.
        """
        filesystems = get_filesystems()
        if not filesystems:
            return {
                "message": "No filesystem exists",
                "data": None,
                "error": "Not found"
            }, http_client.NOT_FOUND
            
        return {
                "message": "Successfully fetched filesystems details",
                "data": filesystems
            }, http_client.OK
    
    @token_required
    def post(self):
        """
        Method to create a new filesystem
        """
        input_data = request.get_data().decode('utf-8')
        if not input_data:
            return {
                "message": "Please provide filesystem details",
                "data": None,
                "error": "Bad request"
            }, http_client.BAD_REQUEST
        
        data = json.loads(input_data)            
        filesystems = get_filesystems()
        for filesystem in filesystems:
            if filesystem.get("filesystem") == data.get("filesystem"):
                return {
                    "message": "filesystem already exists",
                    "data": None,
                    "error": "Conflict"
                }, http_client.BAD_REQUEST

        filesystems.append(data)
        save_filesystems(filesystems)
        return {
                "message": "Successfully created a new filesystem",
                "data": data
            }, http_client.CREATED
        
class FileSystem(flask_restful.Resource):
    @token_required
    def get(self, filesystem_name):
        """
        Method to fetch a specific filesystem
        """
        filesystems = get_filesystems()
        for filesystem in filesystems:
            if filesystem.get("filesystem") == filesystem_name:
                return {
                    "message": "Successfully fetched filesystem details",
                    "data": filesystem
                }, http_client.OK
        return {
                "message": "Filesystem does not exists",
                "data": None,
                "error": "Not found"
            }, http_client.NOT_FOUND
    
    @token_required
    def put(self, filesystem_name):
        """
        Method to modify an existing filesystem.
        """
        filesystems = get_filesystems()
        for filesystem in filesystems:
            if filesystem.get("filesystem") == filesystem_name:
                return {
                    "message": "Successfully fetched filesystem details",
                    "data": filesystem
                }, http_client.OK
        return {
                "message": "Filesystem does not exists",
                "data": None,
                "error": "Not found"
            }, http_client.NOT_FOUND
        
    @token_required
    def delete(self, filesystem_name):
        """
        Method delete an existing filesystem
        """
        filesystems = get_filesystems()
        for index, filesystem in enumerate(filesystems):
            if filesystem.get("filesystem") == filesystem_name:
                del filesystems[index]
                save_filesystems(filesystems)
                return {
                    "message": "Successfully deleted the filesystem",
                    "data": filesystem
                }, http_client.OK
        return {
                "message": "Filesystem does not exists",
                "data": None,
                "error": "Not found"
            }, http_client.NOT_FOUND