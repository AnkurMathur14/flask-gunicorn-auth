import json
import flask_restful
from flask import request
from six.moves import http_client

from models.filesystems import FSManager
from utilities.auth_middleware import token_required

class FileSystemList(flask_restful.Resource):
    @token_required
    def get(self):
        """
        Method to fetch all the filesystems.
        """
        filesystems = FSManager().get_all()
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
        filesystem = FSManager().create(**data)
        if not filesystem:
            return {
                "message": "Filesystem already exists",
                "data": None,
                "error": "Conflict"
            }, http_client.BAD_REQUEST
        return {
                "message": "Filesystem has been created",
                "data": filesystem
            }, http_client.CREATED

        
class FileSystem(flask_restful.Resource):
    @token_required
    def get(self, fs_id):
        """
        Method to fetch a specific filesystem
        """
        filesystem = FSManager().get_by_id(fs_id)
        if not filesystem:
            return {
                "message": "Filesystem does not exists",
                "data": None,
                "error": "Not found"
            }, http_client.NOT_FOUND

        return {
            "message": "Successfully fetched filesystem details",
            "data": filesystem
        }, http_client.OK

    
    @token_required
    def put(self, fs_id):
        """
        Method to modify an existing filesystem.
        """
        input_data = request.get_data().decode('utf-8')
        if not input_data:
            return {
                "message": "Please provide filesystem details",
                "data": None,
                "error": "Bad request"
            }, http_client.BAD_REQUEST
        
        data = json.loads(input_data) 
        filesystem = FSManager().update(fs_id, **data)
        if not filesystem:
            return {
                "message": "Filesystem does not exists",
                "data": None,
                "error": "Not found"
            }, http_client.NOT_FOUND

        return {
            "message": "The filesystem has been updated",
            "data": filesystem
        }, http_client.OK
        
    @token_required
    def delete(self, fs_id):
        """
        Method delete an existing filesystem
        """
        filesystem = FSManager().delete(fs_id)
        if not filesystem:
            return {
                "message": "Filesystem does not exists",
                "data": None,
                "error": "Not found"
            }, http_client.NOT_FOUND

        return {
            "message": "The filesystem has been deleted",
            "data": None
        }, http_client.OK