#!/usr/bin/env python
# -*- coding:utf-8 -*-

from .apiVersionResource import apiversion_blueprint
from .healthCheckResource import healthcheck_blueprint
from .fileStorageResource import fileStorage_blueprint


def init_router(app):
    from api_1_0.apiVersionResource import apiversion_blueprint
    app.register_blueprint(apiversion_blueprint, url_prefix="")

    # healthCheck blueprint register
    from api_1_0.healthCheckResource import healthcheck_blueprint
    app.register_blueprint(healthcheck_blueprint, url_prefix="")

    from api_1_0.fileStorageResource import fileStorage_blueprint
    app.register_blueprint(fileStorage_blueprint, url_prefix="")