#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Api
from flask import request

from . import healthcheck_blueprint
from api_1_0.healthCheckResource.healthCheckOtherResource import HealthCheckOtherResource

api = Api(healthcheck_blueprint)


@healthcheck_blueprint.before_request
def healthz_validation():
    print('in health check ' + request.path)
    if request.method != 'GET':
        return '', 405
    if len(request.args) > 0:
        return '', 400

@healthcheck_blueprint.route('/healthz', methods=['GET'], endpoint='Healthz')
def healthz():
    return HealthCheckOtherResource.api_health_check()

@healthcheck_blueprint.route('/cicd', methods=['GET'], endpoint='CiCd')
def cicdtest():
    return HealthCheckOtherResource.cicd_test()

@healthcheck_blueprint.route('/cicd2', methods=['GET'], endpoint='CiCd2')
def cicdtest():
    return HealthCheckOtherResource.cicd_test()