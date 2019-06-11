# coding: utf-8
import json
from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class ToDo(Base):
    __tablename__ = 'todo'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    done = Column(Integer)
    author_ip = Column(String(40))
    created_date = Column(DateTime, server_default=func.now())
    done_date = Column(String(50))

