#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
import math
import json

from flask import request
from sqlalchemy import or_

from app import db
from models.healthCheck import HealthCheck
from utils import commons
from utils.cloudwatch_integration import metrics_timer
from utils.response_code import RET, error_map_EN
from utils.loggings import loggings
from models import BaseModel


class HealthCheckController(HealthCheck,BaseModel):

    # add
    @classmethod
    @metrics_timer("db.query.healthz.add")
    def add(cls, **kwargs):
        # if request.method != "POST":
        #     return {"code": RET.METHODERR, "message": "Invalid method"}
        from utils.generate_id import GenerateID
        CheckID = GenerateID.create_random_id()
        
        try:
            model = HealthCheck(
                # CheckID=CheckID,
                Datetime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                
            )
            db.session.add(model)
            db.session.commit()
            results = {
                'add_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'CheckID': model.CheckID,
                
            }
            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': results}
            
        except Exception as e:
            db.session.rollback()
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {'error': str(e)}}
        finally:
            db.session.close()

    # get
    @metrics_timer("db.query.healthz.get")
    @classmethod
    def get(cls, **kwargs):
        try:
            filter_list = [cls.IsDeleted == 0]
            if kwargs.get('CheckID'):
                filter_list.append(cls.CheckID == kwargs['CheckID'])
            else:
                if kwargs.get('Datetime'):
                    filter_list.append(cls.Datetime == kwargs.get('Datetime'))
                

            page = int(kwargs.get('Page', 1))
            size = int(kwargs.get('Size', 10))
            
            healthCheck_info = db.session.query(cls).filter(*filter_list)
            
            count = healthCheck_info.count()
            pages = math.ceil(count / size)
            healthCheck_info = healthCheck_info.limit(size).offset((page - 1) * size).all()
   
            #results = commons.query_to_dict(healthCheck_info)
            results = cls.to_dict(healthCheck_info)
            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'totalCount': count, 'totalPage': pages, 'data': results}
            
        except Exception as e:
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {'error': str(e)}}
        finally:
            db.session.close()

    # delete
    @metrics_timer("db.query.healthz.delete")
    @classmethod
    def delete(cls, **kwargs):
        try:
            filter_list = [cls.IsDeleted == 0]
            if kwargs.get('CheckID'):
                primary_key_list = []
                for primary_key in str(kwargs.get('CheckID')).replace(' ', '').split(','):
                    primary_key_list.append(cls.CheckID == primary_key)
                filter_list.append(or_(*primary_key_list))
                
            else:
                if kwargs.get('Datetime'):
                    filter_list.append(cls.Datetime == kwargs.get('Datetime'))
                
            res = db.session.query(cls).filter(*filter_list).with_for_update()

            results = {
                'delete_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'CheckID': []
            }
            for query_model in res.all():
                results['CheckID'].append(query_model.CheckID)

            res.update({'IsDeleted': 1})
            db.session.commit()

            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': results}

        except Exception as e:
            db.session.rollback()
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {'error': str(e)}}
        finally:
            db.session.close()
    
    # update
    @metrics_timer("db.query.healthz.get")
    @classmethod
    def update(cls, **kwargs):
        try:
            
            
            filter_list = [cls.IsDeleted == 0]
            filter_list.append(cls.CheckID == kwargs.get('CheckID'))
            
            res = db.session.query(cls).filter(*filter_list).with_for_update()
            if res.first():
                results = {
                    'update_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'CheckID': res.first().CheckID,
                
                }
                
                res.update(kwargs)
                db.session.commit()
            else:
                results = {
                    'error': 'data dose not exist'
                }

            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': results}

        except Exception as e:
            db.session.rollback()
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {'error': str(e)}}
        finally:
            db.session.close()

    # batch add
    @classmethod
    def add_list(cls, **kwargs):
        param_list = kwargs.get('HealthCheckList')
        model_list = []
        for param_dict in param_list:
            from utils.generate_id import GenerateID
            CheckID = GenerateID.create_random_id()
            
            model = HealthCheck(
                CheckID=CheckID,
                Datetime=param_dict.get('Datetime'),
                
            )
            model_list.append(model)
        
        try:
            db.session.add_all(model_list)
            db.session.commit()
            results = {
                'added_records': [],
                'add_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            for model in model_list:
                added_record = {}
                added_record['CheckID'] = model.CheckID
                
                results['added_records'].append(added_record)
                
            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': results}
            
        except Exception as e:
            db.session.rollback()
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {'error': str(e)}}
        finally:
            db.session.close()
