#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Api

from . import healthcheck_blueprint
from api_1_0.healthCheckResource.healthCheckResource import HealthCheckResource
from api_1_0.healthCheckResource.healthCheckOtherResource import HealthCheckOtherResource

api = Api(healthcheck_blueprint)

# api.add_resource(HealthCheckResource, '/healthCheck/<CheckID>', '/healthCheck', endpoint='HealthCheck')
api.add_resource(HealthCheckResource, '/healthCheck/<CheckID>', '/healthCheck', endpoint='HealthCheck')



@healthcheck_blueprint.route('/healthcheck/update/<CheckID>', methods=['PUT'], endpoint='HealthCheckUpdate')
def update(CheckID):
    return HealthCheckOtherResource.sensitive_update(CheckID)

@healthcheck_blueprint.route('/healthz', methods=['GET'], endpoint='Healthz')
def healthz():
    return HealthCheckOtherResource.api_health_check()