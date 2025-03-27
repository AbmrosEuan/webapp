#!/usr/bin/env python
# -*- coding:utf-8 -*-

import uuid, datetime
import boto3
import os
import io
from flask_restful import Resource, reqparse
from flask import jsonify, request, Response

from utils.cloudwatch_integration import metrics_timer
from utils.generate_id import GenerateID
from controller.fileStorageController import FileStorageController
from utils import commons
from utils.response_code import RET, error_map_EN
from dotenv import load_dotenv, find_dotenv
from app.setting import Settings
from botocore.exceptions import NoCredentialsError


env_path = "./webapp.env"

load_dotenv(find_dotenv(env_path))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class FileStorageOtherResource(Resource):

    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=Settings.AWS_S3_REGION_NAME,
    )


    @classmethod
    @metrics_timer("api.s3.fileUpload")
    def upload_file(cls):

        if request.method != 'POST':
            return Response(status=405)

        if 'file' not in request.files:
            print("No file provided")
            return Response("No file provided", status=400)

        file = request.files['file']

        if file.filename == '':
            print("No file selected")
            return Response("No file selected", status=400)

        file_id = str(uuid.uuid4()) + "_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = file_id + "_" + file.filename
        user_id = "123456"

        # Upload to S3
        bucket_name = Settings.AWS_S3_BUCKET_NAME
        try:
            cls.s3_client.upload_fileobj(
                file,
                bucket_name,
                file_name,
            )
            print('File successfully uploaded to S3')
        except NoCredentialsError:
            print('AWS credentials not properly configured')
            return Response("AWS credentials not properly configured", status=500)
        except Exception as e:
            print(f"File upload failed: {e}")
            return Response(f"File upload failed: {e}", status=500)

        # add metadata to db
        url = f"s3://{bucket_name}/{file_name}"
        kwargs = {
            "file_id": file_id,
            "file_name": file_name,
            "url": url,
            "user_id": user_id
        }

        res = FileStorageController.add(**kwargs)
        res = res['data']

        return jsonify(res), 200

    @classmethod
    @metrics_timer("api.s3.get_file")
    def get_file_info(cls):

        kwargs = request.args
        print(kwargs)
        if kwargs.get('file_id') is None:
            return '', 400

        res = FileStorageController.get(**kwargs)
        if res['code'] == RET.OK and res['data']:
            res = res['data'][0]
            file_info = {
                'file_name': res['FileName'],
                'id': res['FileID'],
                'url': res['FileUrl'],
                'upload_date': res['Datetime']
            }
            return file_info, 200
        else:
            return '', 404


    @classmethod
    @metrics_timer("api.s3.delete_file")
    def file_delete(cls):
        kwargs = request.args
        print(kwargs)
        if kwargs.get('file_id') is None:
            return '', 404

        query_res = FileStorageController.get(**kwargs)

        if query_res['code'] == RET.OK and query_res['data']:
            res = FileStorageController.delete(**kwargs)
            if res['code'] == RET.OK:
                return res['data'], 204
            else:
                return '', 503

        else:
            return '', 404