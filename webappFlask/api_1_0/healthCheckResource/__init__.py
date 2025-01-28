#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint

healthcheck_blueprint = Blueprint('healthCheck', __name__)

from . import urls
