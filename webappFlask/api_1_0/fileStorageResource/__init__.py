#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint

fileStorage_blueprint = Blueprint('fileStorage', __name__)

from . import urls
