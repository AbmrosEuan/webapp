#!/usr/bin/env python
# -*- coding:utf-8 -*- 

from flask_restful import Resource, reqparse
from flask import jsonify

from controller.healthCheckController import HealthCheckController
from utils import commons
from utils.response_code import RET, error_map_EN
import json


class HealthCheckResource(Resource):

    # get
    @classmethod
    def get(cls, CheckID=None):
        if CheckID:
            kwargs = {
                'CheckID': CheckID
            }

            res = HealthCheckController.get(**kwargs)
            if res['code'] == RET.OK:
                return jsonify(code=res['code'], message=res['message'], data=res['data'])
            else:
                return jsonify(code=res['code'], message=res['message'], data=res['data'])

        parser = reqparse.RequestParser()
        parser.add_argument('AutoID', location='args', required=False, help='AutoID参数类型不正确或缺失')
        parser.add_argument('CheckID', location='args', required=False, help='CheckID参数类型不正确或缺失')
        parser.add_argument('IsDeleted', location='args', required=False, help='IsDeleted参数类型不正确或缺失')
        parser.add_argument('Datetime', location='args', required=False, help='Datetime参数类型不正确或缺失')
        
        parser.add_argument('Page', location='args', required=False, help='Page参数类型不正确或缺失')
        parser.add_argument('Size', location='args', required=False, help='Size参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)

        res = HealthCheckController.get(**kwargs)
        if res['code'] == RET.OK:
            return jsonify(code=res['code'], message=res['message'], data=res['data'], totalPage=res['totalPage'], totalCount=res['totalCount'])
        else:
            return jsonify(code=res['code'], message=res['message'], data=res['data']) 

    
    # delete
    @classmethod
    def delete(cls, CheckID=None):
        if CheckID:
            kwargs = {
                'CheckID': CheckID
            }

        else:
            return jsonify(code=RET.PARAMERR, message=error_map_EN[RET.PARAMERR], data='id不能为空')

        res = HealthCheckController.delete(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])

    
    # put
    @classmethod
    def put(cls, CheckID):
        if not CheckID:
            return jsonify(code=RET.NODATA, message='primary key missed', error='primary key missed')

        parser = reqparse.RequestParser()
        parser.add_argument('Datetime', location='form', required=False, help='Datetime参数类型不正确或缺失')
        
        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)
        kwargs['CheckID'] = CheckID

        res = HealthCheckController.update(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])

    
    # add
    @classmethod
    def post(cls):
        '''
        HealthCheckList: Pass in values in JSON format to batch add
        eg.[{k1:v1,k2:v2,...},...]
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('HealthCheckList', type=str, location='form', required=False, help='HealthCheckList参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)

        if kwargs.get('HealthCheckList'):
            kwargs['HealthCheckList'] = json.loads(kwargs['HealthCheckList'])
            for data in kwargs['HealthCheckList']:
                for key in ['IsDeleted']:
                    data.pop(key, None)
            res = HealthCheckController.add_list(**kwargs)

        else:
            parser.add_argument('Datetime', location='form', required=False, help='Datetime参数类型不正确或缺失')
            
            kwargs = parser.parse_args()
            kwargs = commons.put_remove_none(**kwargs)

            res = HealthCheckController.add(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])
