#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
   应用初始化文件模板
"""
from sqlalchemy import create_engine, Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import create_database, database_exists
from flask import Flask
from flask_session import Session
from .setting import Settings
from  models import db



# 工厂模式创建app应用对象
def create_app(run_mode):
    """
    创建flask的应用对象
    :param run_mode: string 配置模式的名字  （"develop", "product", "test"）
    :return:
    """
    
    app = Flask(__name__)

    # 根据配置模式的名字获取配置参数的类
    app.config.from_object(Settings.get_setting(run_mode))


    db_name = Settings.DATABASE
    db_url = Settings.SQLALCHEMY_DATABASE_URI

    engine = create_engine(db_url, echo=True)
    if not database_exists(engine.url):
        create_database(engine.url)
        print(f"数据库 {db_name} 创建成功！")
    else:
        print(f"数据库 {db_name} 已经存在。")


    # 使用app初始化db
    db.init_app(app)

    # 在数据库中创建所有表
    with app.app_context():
        db.create_all()
        print("所有数据表创建完毕")

    # 利用Flask_session将数据保存的session中
    Session(app)



    # 调用resource层中定义的方法，初始化所有路由(注册)蓝图
    from api_1_0 import init_router
    init_router(app)
    
    return app
