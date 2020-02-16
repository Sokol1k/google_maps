from sqlalchemy import Column, String, TIMESTAMP, Integer, text, DECIMAL
from sqlalchemy.ext.declarative import declarative_base


class CitiesModel(declarative_base()):
    __tablename__ = 'cities'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    city = Column('city', String, nullable=False, unique=True, index=True)
    sw_latitude = Column('sw_latitude', DECIMAL, nullable=False)
    sw_longitude = Column('sw_longitude', DECIMAL, nullable=False)
    ne_latitude = Column('ne_latitude', DECIMAL, nullable=False)
    ne_longitude = Column('ne_longitude', DECIMAL, nullable=False)
    create_at = Column('created_at', TIMESTAMP,
                       server_default=text('now()'), nullable=False)
    updated_at = Column('updated_at', TIMESTAMP,
                        server_default=text('now()'), server_onupdate=text('now()'), nullable=False)
