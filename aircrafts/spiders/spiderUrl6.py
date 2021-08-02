import scrapy
from scrapy_splash import SplashRequest
from ..items import AircraftsItem
from scrapy.http import Request

import json

class BusinessairSpider(scrapy.Spider):
    name = 'businessair'
    
    
    def start_requests(self):
        url = "https://www.businessair.com/jet-aircraft"
        splash_args = {'timeout': 85, 'wait': 2.5}

        yield SplashRequest(url=url, callback=self.parse_pages, args=splash_args, dont_filter=True)

    def parse_pages(self, response):
        splash_args = {'timeout': 85, 'wait': 2.5}
        aircrafts = response.xpath('//a[text()="View »"]/@href').extract()
        for aircraft in aircrafts:
            make = aircraft.split('/')[2]
            model = aircraft.split('/')[3]
            source = "https://www.businessair.com"+aircraft
            aircraftsItem = AircraftsItem()
            aircraftsItem['source'] = source
            aircraftsItem['make'] = make
            aircraftsItem['model'] = model

            #print("https://www.businessair.com"+aircraft)
            yield SplashRequest(url="https://www.businessair.com"+aircraft, callback=self.parse, args=splash_args, dont_filter=True, meta={"aircraftsItem": aircraftsItem})
            
        
        href = response.xpath('//a[text()="›"]/@href').extract_first()
        if href:
            next_url = "https://www.businessair.com" + href
            yield SplashRequest(url=next_url, callback=self.parse_pages, args=splash_args, dont_filter=True)
    
    
            
    def parse(self, response):

        infos = response.css('.even::text').extract()
        if len(infos)>2:
            year = infos[1]
            time = infos[2]
            serial_number = infos[3]
            price = infos[5]
        dealer = response.css('.views-field-title-1 a::text').extract_first()
            
        aircraftsItem = response.meta.get('aircraftsItem')        
        aircraftsItem['year'] = year
        aircraftsItem['time'] = time
        aircraftsItem['serial_Number'] = serial_number
        aircraftsItem['price'] = price
        aircraftsItem['dealer'] = dealer
        yield aircraftsItem

        