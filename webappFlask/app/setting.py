#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
  应用的配置加载项
"""

import os
from dotenv import load_dotenv, find_dotenv
from configparser import ConfigParser
from urllib import parse

# load secret
env_path = "./webapp.env"

load_dotenv(find_dotenv(env_path))

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 配置文件和数据文件目录
CONFIG_DIR = os.path.join(BASE_DIR, 'config')


class Settings(object):
    CONFIG = ConfigParser()

    @classmethod
    def get_setting(cls, runMode):
        cls.CONFIG.read(os.path.join(CONFIG_DIR, runMode + '_config.conf'), encoding='utf-8')

        # 秘钥-laptop
        # cls.SECRET_KEY = cls.CONFIG['BASIC']['secret_key']
        # cls.AES_SECRET_KEY = cls.CONFIG['AES']['secret_key']
        # cls.PUBLIC_KEY = cls.CONFIG['RSA']['public_key']
        # cls.PRIVATE_KEY = cls.CONFIG['RSA']['private_key']

        # 秘钥
        cls.SECRET_KEY = os.getenv('WEBAPP_SECRET_KEY')
        cls.AES_SECRET_KEY = os.getenv('WEBAPP_AES_SECRET_KEY')
        cls.PUBLIC_KEY = os.getenv('WEBAPP_PUBLIC_KEY')
        cls.PRIVATE_KEY = os.getenv('WEBAPP_PRIVATE_KEY')

        # debug模式
        # DEBUG = DEVELOP_CONFIG.getboolean('STATIC_CONFIG', 'DEBUG')

        # 数据库配置-laptop
        cls.DIALECT = cls.CONFIG['DATABASE']['dialect']
        cls.DRIVER = cls.CONFIG['DATABASE']['driver']

        cls.PORT = cls.CONFIG['DATABASE']['port']
        cls.DATABASE = cls.CONFIG['DATABASE']['database']




        cls.USERNAME = os.getenv('MYSQL_USERNAME')
        cls.PASSWORD = os.getenv('MYSQL_PASSWORD')
        print(cls.USERNAME, cls.PASSWORD, cls.PRIVATE_KEY)

        # aws RDB
        cls.ENVIRONMENT = os.getenv('ENVIRONMENT')

        cls.HOST = os.getenv('DB_HOST')

        # elif cls.ENVIRONMENT == 'server':
        #     cls.HOST = os.getenv('DB_HOST')
        #     cls.READER = os.getenv('DB_READER')
        #     cls.SQLALCHEMY_BINDS = {
        #         'reader': '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(
        #             cls.DIALECT, cls.DRIVER, cls.USERNAME, parse.quote_plus(cls.PASSWORD), cls.READER, cls.PORT,
        #             cls.DATABASE)
        #     }

        cls.SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(
            cls.DIALECT, cls.DRIVER, cls.USERNAME, parse.quote_plus(cls.PASSWORD), cls.HOST, cls.PORT, cls.DATABASE)


        cls.SQLALCHEMY_TRACK_MODIFICATIONS = cls.CONFIG.getboolean('DATABASE', 'sqlalchemy_track_modifications')

        # 数据库池的大小。 默认与数据库引擎的值相同 (通常为 5)
        cls.SQLALCHEMY_POOL_SIZE = int(cls.CONFIG['DATABASE']['sqlalchemy_pool_size'])

        # 控制连接池达到最大大小后还可以创建的连接数，当这些附加连接返回到连接池时，它们将会被断开并丢弃。
        cls.SQLALCHEMY_MAX_OVERFLOW = int(cls.CONFIG['DATABASE']['sqlalchemy_max_overflow'])

        # token的有效期,单位：秒
        cls.TOKEN_EXPIRES = int(cls.CONFIG['BASIC']['token_expires'])

        # AWS confi
        cls.AWS_S3_REGION_NAME =os.getenv('AWS_S3_REGION_NAME')
        cls.AWS_S3_BUCKET_NAME = os.getenv('AWS_S3_BUCKET_NAME')
        cls.AWS_S3_BASE_URL = f"https://{cls.AWS_S3_BUCKET_NAME}.s3.{cls.AWS_S3_REGION_NAME}.amazonaws.com"

        #Log config
        cls.FLASK_APP_LOG = cls.CONFIG['LOG']['flask_log']

        return cls

