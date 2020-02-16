import logging
import os
from database.Connection import Connection
from scrapy.commands import ScrapyCommand

logger = logging.getLogger(__name__)


class SectorizationCommand(ScrapyCommand):
    def __init__(self, *a, **kw):
        self.db = Connection()

    def run(self, args, opts):
        if args and (len(args) == 4):
            try:
                data = {}
                data['city'] = args[0]
                ne = args[1].split(', ')
                data['ne'] = [float(ne[0]), float(ne[1])]
                sw = args[2].split(', ')
                data['sw'] = [float(sw[0]), float(sw[1])]
                data['keyword'] = args[3]
                logger.info('The data is correct!')
            except:
                logger.error('The data is not correct!')
                return

            city = {
                'city': data['city'],
                'sw_latitude': data['sw'][0],
                'sw_longitude': data['sw'][1],
                'ne_latitude': data['ne'][0],
                'ne_longitude': data['ne'][1]
            }

            result = self.db.set_city(city)
            if result is None:
                return

            city_id = self.db.get_city_id(city['city'])
            if city_id is None:
                return

            result = self.db.set_keyword({'keyword': data['keyword']})
            if result is None:
                return

            keyword_id = self.db.get_keyword_id(data['keyword'])
            if keyword_id is None:
                return

            sectors = self.sectors_generation(data['ne'], data['sw'])

            if sectors:
                for sector in sectors:
                    sector['city_id'] = city_id
                    sector['keyword_id'] = keyword_id
                    sector['unique_center'] = str(
                        sector['center_latitude']) + str(sector['center_longitude'])
                    result = self.db.set_sector(sector)
                    if result is None:
                        logger.error(
                            'An error occurred while adding a sector to the database!')
                        return
                logger.info('All sectors added to the database!')
                print('SUCCESS!')
                return
            else:
                logger.error('Sector split error!')
                return

        else:
            logger.error('The data is not correct!')
            return

    def sector(self, x, y, step):
        sector = {}
        sector['ne_latitude'] = float("{0:.6f}".format(x + step))
        sector['ne_longitude'] = float("{0:.6f}".format(y + step))
        sector['center_latitude'] = float("{0:.6f}".format(x + (step/2)))
        sector['center_longitude'] = float("{0:.6f}".format(y + (step/2)))
        sector['sw_latitude'] = float("{0:.6f}".format(x))
        sector['sw_longitude'] = float("{0:.6f}".format(y))
        return sector

    def sectors_generation(self, ne, sw):
        step = float(os.getenv('STEP_KM'))
        sectors = []
        start_y = sw[1]
        while True:
            if start_y + step < ne[1]:
                start_x = sw[0]
                while True:
                    if start_x + step < ne[0]:
                        sectors.append(self.sector(start_x, start_y, step))
                        start_x = start_x + step
                    elif start_x + step == ne[0]:
                        sectors.append(self.sector(start_x, start_y, step))
                        break
                    else:
                        sectors.append(self.sector(start_x, start_y, step))
                        break
                start_y = start_y + step
            elif start_y + step == ne[1]:
                start_x = sw[0]
                while True:
                    if start_x + step < ne[0]:
                        sectors.append(self.sector(start_x, start_y, step))
                        start_x = start_x + step
                    elif start_x + step == ne[0]:
                        sectors.append(self.sector(start_x, start_y, step))
                        break
                    else:
                        sectors.append(self.sector(start_x, start_y, step))
                        break
                break
            else:
                start_x = sw[0]
                while True:
                    if start_x + step < ne[0]:
                        sectors.append(self.sector(start_x, start_y, step))
                        start_x = start_x + step
                    elif start_x + step == ne[0]:
                        sectors.append(self.sector(start_x, start_y, step))
                        break
                    else:
                        sectors.append(self.sector(start_x, start_y, step))
                        break
                break
        return sectors

# scrapy SectorizationCommand "Los Angeles" "34.337702, -118.146724" "33.692288, -118.674068" "restaurant" -L WARNING
