#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
import math
import json


from flask import request
from sqlalchemy import or_

from app import db
from models.fileInfo import FileInfo
from utils import commons
from utils.cloudwatch_integration import metrics_timer
from utils.response_code import RET, error_map_EN
from utils.loggings import loggings
from models import BaseModel


class FileStorageController(FileInfo, BaseModel):

    # add

    @classmethod
    @metrics_timer("db.query.S3file.add")
    def add(cls, **kwargs):

        try:
            model = FileInfo(
                FileID=kwargs.get('file_id'),
                FileName=kwargs.get("file_name"),
                FileS3ID=kwargs.get("s3_id"),
                Datetime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                FileUrl=kwargs.get("url"),
                UserID = kwargs.get("user_id"),
            )
            db.session.add(model)
            db.session.commit()
            results = {
                'file_name': model.FileName,
                'id': model.FileID,
                'url': model.FileUrl,
                'upload_time': model.Datetime,
            }
            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': results}

        except Exception as e:
            db.session.rollback()
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {'error': str(e)}}
        finally:
            db.session.close()

    # get

    @classmethod
    @metrics_timer("db.query.S3file.get")
    def get(cls, **kwargs):
        try:
            filter_list = []
            if kwargs.get('file_id'):
                filter_list.append(cls.FileID == kwargs['file_id'])

            page = int(kwargs.get('Page', 1))
            size = int(kwargs.get('Size', 10))

            file_info = db.session.query(cls).filter(*filter_list)

            count = file_info.count()
            pages = math.ceil(count / size)
            file_info = file_info.limit(size).offset((page - 1) * size).all()

            # results = commons.query_to_dict(file_info)
            results = cls.to_dict(file_info)
            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'totalCount': count, 'totalPage': pages,
                    'data': results}

        except Exception as e:
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {'error': str(e)}}
        finally:
            db.session.close()

    # delete

    @classmethod
    @metrics_timer("db.query.S3file.delete")
    def delete(cls, **kwargs):
        try:
            filter_list = []
            if kwargs.get('file_id'):
                primary_key_list = []
                for primary_key in str(kwargs.get('file_id')).replace(' ', '').split(','):
                    primary_key_list.append(cls.FileID == primary_key)
                filter_list.append(or_(*primary_key_list))

            res = db.session.query(cls).filter(*filter_list).with_for_update()

            results = {
                'delete_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'file_id': []
            }
            for query_model in res.all():
                results['file_id'].append(query_model.FileID)

            res.delete()

            db.session.commit()

            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': results}

        except Exception as e:
            db.session.rollback()
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {'error': str(e)}}
        finally:
            db.session.close()

