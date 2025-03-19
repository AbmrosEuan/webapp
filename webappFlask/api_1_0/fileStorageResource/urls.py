#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import request
from flask_restful import Api

from . import fileStorage_blueprint

from api_1_0.fileStorageResource.fileStorageOtherResource import FileStorageOtherResource

api = Api(fileStorage_blueprint)

@fileStorage_blueprint.before_request
def fileStorageUpload_before_request():
    if request.endpoint == 'fileStorage.FileStorageUpload' and request.method != 'POST':
        return '', 405

@fileStorage_blueprint.route('/v1/file', methods=['POST'], endpoint='FileStorageUpload')
def upload_file():
    return FileStorageOtherResource.upload_file()




@fileStorage_blueprint.before_request
def fileStorageGet_before_request():
    if request.endpoint == 'fileStorage.FileStorageGet' and request.method != 'GET':
        return '', 405

@fileStorage_blueprint.route('/v1/file', methods=['GET'], endpoint='FileStorageGet')
def get_file_info():
    return FileStorageOtherResource.get_file_info()


@fileStorage_blueprint.before_request
def fileStorageDelete_before_request():
    if request.endpoint == 'fileStorage.FileStorageDelete' and request.method != 'DELETE':
        return '', 405

@fileStorage_blueprint.route('/v1/file', methods=['DELETE'], endpoint='FileStorageDelete')
def file_delete():
    return FileStorageOtherResource.file_delete()