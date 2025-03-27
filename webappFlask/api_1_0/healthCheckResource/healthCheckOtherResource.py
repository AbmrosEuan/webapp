#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Resource, reqparse
from flask import jsonify, request, Response

from controller.healthCheckController import HealthCheckController
from utils import commons
from utils.response_code import RET, error_map_EN
from utils.cloudwatch_integration import metrics_timer, log_request, log_error, logger



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
    @metrics_timer("api.healthz")
    def api_health_check(cls):
        logger.info("Calling api_health_check")

        res = HealthCheckController.add()

        if res['code'] != RET.OK:
            logger.error("Failed to call api_health_check")
            return Response(status=503)

        if res['code'] == RET.OK:
            return Response(status=200)




