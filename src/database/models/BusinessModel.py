from sqlalchemy import Column, String, TIMESTAMP, Integer, text, DECIMAL, BOOLEAN, Float
from sqlalchemy.ext.declarative import declarative_base


class BusinessModel(declarative_base()):
    __tablename__ = 'businesses'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    name = Column('name', String, nullable=False)
    url = Column('url', String, nullable=False, unique=True, index=True)
    category = Column('category', String)
    phone = Column('phone', String)
    website = Column('website', String)
    claimed_business = Column('claimed_business', BOOLEAN)
    rating = Column('rating', Float)
    reviews = Column('reviews', Integer)
    image = Column('image', String)
    latitude = Column('latitude', DECIMAL, nullable=False)
    longitude = Column('longitude', DECIMAL, nullable=False)
    full_address = Column('full_address', String)
    address = Column('address', String)
    city = Column('city', String)
    zipcode = Column('zipcode', String)
    country = Column('country', String)
    create_at = Column('created_at', TIMESTAMP,
                       server_default=text('now()'), nullable=False)
    updated_at = Column('updated_at', TIMESTAMP,
                        server_default=text('now()'), server_onupdate=text('now()'), nullable=False)
