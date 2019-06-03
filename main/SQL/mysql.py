from sqlalchemy import Column, String, Integer,Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from main import app,db
from main.SQL import mysql_config
import json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import Flask



class Image(db.Model):
    id = Column(Integer(), primary_key=True)
    image = Column(String(100))
    time = db.Column(db.DateTime, default=datetime.now())
    __tablename__ = "image"

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict


class Temp(db.Model):
    id = Column(Integer(), primary_key=True)
    humidity = Column(Integer())
    temperature = Column(Integer())
    time = db.Column(db.DateTime, default=datetime.now())
    __tablename__ = "temp"

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict


if __name__ == "__main__":
    db.create_all()
