# coding: utf-8
from . import db, BaseModel


class FileInfo(db.Model):
    __tablename__ = 'fileInfo'

    # AutoID = db.Column(db.BigInteger, primary_key=True, info='CheckID')
    # CheckID = db.Column(db.BigInteger, nullable=False)
    # IsDeleted = db.Column(db.Integer, server_default=db.FetchedValue(), info='0-not deleted; 1-deleted')
    RecordID = db.Column(db.BigInteger, primary_key=True)
    Datetime = db.Column(db.DateTime)
    FileID = db.Column(db.String(255), info='FileID')
    FileName = db.Column(db.String(255), info='FileName')
    FileS3ID = db.Column(db.String(255), info='FileS3ID')
    FileUrl = db.Column(db.String(255), info='FilUurl')
    UserID = db.Column(db.String(255), info='UserID')

