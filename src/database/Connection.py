import logging
import os
from sqlalchemy import create_engine, text, update
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.mysql import insert
from database.models.CitiesModel import CitiesModel
from database.models.KeywordsModel import KeywordsModel
from database.models.SectorsModel import SectorsModel
from database.models.BusinessModel import BusinessModel

logger = logging.getLogger(__name__)


class Connection(object):
    def __init__(self):
        self.engine = create_engine(os.getenv('DATABASE_URL'))
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def __del__(self):
        self.session.close()

    def set_city(self, item):
        insert_stmt = insert(CitiesModel).values(**item)
        on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(**item,
                                                                    updated_at=text('now()'))
        try:
            self.session.execute(on_duplicate_key_stmt)
            self.session.commit()
            logger.info('City "%s" added to database', item['city'])
            return item
        except:
            self.session.rollback()
            logger.error('City "%s" ​​not added to database', item['city'])
            return None

    def get_city_id(self, city):
        try:
            item = self.session.query(CitiesModel).filter_by(city=city).first()
            return item.id
        except:
            logger.error('The city "%s" does not exist in the database', city)
            return None

    def set_keyword(self, item):
        keyword = self.session.query(KeywordsModel).filter_by(
            keyword=item['keyword']).first()
        if not keyword:
            keyword = KeywordsModel()
            keyword.keyword = item['keyword']
            try:
                self.session.add(keyword)
                self.session.commit()
                logger.info('Keyword "%s" added to database', item['keyword'])
                return item
            except:
                self.session.rollback()
                logger.error(
                    'Keyword "%s" ​​not added to database', item['keyword'])
                return None
        else:
            logger.info(
                'Keyword "%s" already exists in the database', item['keyword'])
            return item

    def get_keyword_id(self, keyword):
        try:
            item = self.session.query(KeywordsModel).filter_by(
                keyword=keyword).first()
            return item.id
        except:
            logger.error(
                'The keyword "%s" does not exist in the database', keyword)
            return None

    def set_sector(self, item):
        insert_stmt = insert(SectorsModel).values(**item)
        on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(**item,
                                                                    updated_at=text('now()'))
        try:
            self.session.execute(on_duplicate_key_stmt)
            self.session.commit()
            return item
        except:
            self.session.rollback()
            return None

    def get_keyword_by_id(self, id):
        try:
            keyword = self.session.query(
                KeywordsModel).filter_by(id=id).first()
            return keyword.keyword
        except:
            logger.error('Keyword with such id not found!')
            return None

    def get_sector(self):
        try:
            sector = self.session.query(
                SectorsModel).filter_by(status=0).first()
            sector.keyword = self.get_keyword_by_id(sector.keyword_id)
            if sector.keyword is None:
                return False
            return sector
        except:
            logger.error('Sector not found!')
            return False

    def change_sector_status(self, item):
        sector = update(SectorsModel).where(SectorsModel.id == item['id']).values(
            status=item['status'], updated_at=text('now()'))

        try:
            self.session.execute(sector)
            self.session.commit()
            return item['id']
        except:
            self.session.rollback()
            logger.error(
                'Sector with id = "%s" status not changed', item['id'])
            return None

    def add_item(self, item):
        insert_stmt = insert(BusinessModel).values(**item)
        on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(**item,
                                                                    updated_at=text('now()'))
        try:
            self.session.execute(on_duplicate_key_stmt)
            self.session.commit()
            logger.info('Business "%s" added to database', item['name'])
        except:
            self.session.rollback()
            logger.error('Business "%s" ​​not added to database', item['name'])
            return None
