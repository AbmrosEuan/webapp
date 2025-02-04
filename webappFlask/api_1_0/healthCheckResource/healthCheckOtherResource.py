#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Resource, reqparse
from flask import jsonify, request, Response

from controller.healthCheckController import HealthCheckController
from utils import commons
from utils.response_code import RET, error_map_EN




class HealthCheckOtherResource(Resource):

    @classmethod
    def sensitive_update(cls, CheckID):
        if not CheckID:
            return jsonify(code=RET.NODATA, message='primary key missed', error='primary key missed')

        parser = reqparse.RequestParser()
        parser.add_argument('IsDeleted', location='form', required=False, help='IsDeleted参数类型不正确或缺失')
        
        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)
        kwargs['CheckID'] = CheckID

        res = HealthCheckController.update(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])

    @classmethod
    def api_health_check(cls):
        if request.args or request.form:
            print(request.args)
            return Response(status=400)

        if request.method == "GET" and request.get_data():
            return Response(status=400)

        if request.method != 'GET':
            return Response(status=405)


        res = HealthCheckController.add()

        if res['code'] != RET.OK:
            # return jsonify(code=res['code']), 503
            return Response(status=503)

        if res['code'] == RET.OK:
            return Response(status=200)


        # return jsonify(code=res['code'])

