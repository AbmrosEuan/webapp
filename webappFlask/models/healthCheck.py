# coding: utf-8
from . import db, BaseModel


class HealthCheck(db.Model):
    __tablename__ = 'healthCheck'

    # AutoID = db.Column(db.BigInteger, primary_key=True, info='CheckID')
    # CheckID = db.Column(db.BigInteger, nullable=False)
    # IsDeleted = db.Column(db.Integer, server_default=db.FetchedValue(), info='0-not deleted; 1-deleted')

    CheckID = db.Column(db.BigInteger, primary_key=True, info='CheckID')
    Datetime = db.Column(db.DateTime)
