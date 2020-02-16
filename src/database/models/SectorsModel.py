from sqlalchemy import Column, String, TIMESTAMP, Integer, text, DECIMAL
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.ext.declarative import declarative_base


class SectorsModel(declarative_base()):
    __tablename__ = 'sectors'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    city_id = Column('city_id', Integer, nullable=False)
    keyword_id = Column('keyword_id', Integer, nullable=False)
    status = Column('status', Integer, nullable=False, default=0)
    unique_center = Column('unique_center', String,
                           nullable=False, unique=True, index=True)
    sw_latitude = Column('sw_latitude', DECIMAL, nullable=False)
    sw_longitude = Column('sw_longitude', DECIMAL, nullable=False)
    center_latitude = Column('center_latitude', DECIMAL, nullable=False)
    center_longitude = Column('center_longitude', DECIMAL, nullable=False)
    ne_latitude = Column('ne_latitude', DECIMAL, nullable=False)
    ne_longitude = Column('ne_longitude', DECIMAL, nullable=False)
    create_at = Column('created_at', TIMESTAMP,
                       server_default=text('now()'), nullable=False)
    updated_at = Column('updated_at', TIMESTAMP,
                        server_default=text('now()'), server_onupdate=text('now()'), nullable=False)
