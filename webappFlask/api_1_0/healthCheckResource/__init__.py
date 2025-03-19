#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint, request
from flask import current_app
healthcheck_blueprint = Blueprint('healthCheck', __name__)

from . import urls
