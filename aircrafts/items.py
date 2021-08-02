import scrapy
from scrapy.item import Field

import sys
sys.path.append("..")


class AircraftsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    make = Field()
    model = Field()
    year = Field()
    serial_Number = Field()
    time = Field()
    price = Field()
    location = Field()
    dealer = Field()
    source = Field()
    location = Field()