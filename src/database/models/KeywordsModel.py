from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

class KeywordsModel(declarative_base()):
    __tablename__ = 'keywords'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    keyword = Column('keyword', String, nullable=False, unique=True, index=True)
    