import scrapy
from scrapy_splash import SplashRequest
from ..items import AircraftsItem
from scrapy.http import Request

import json

class GlobalairSpider(scrapy.Spider):
    name = 'globalair'
    
    
    def start_requests(self):
        url = "https://www.globalair.com/aircraft-for-sale/Private-Jet"
        splash_args = {'timeout': 85, 'wait': 2.5}

        yield SplashRequest(url=url, callback=self.parse_pages, args=splash_args, dont_filter=True, meta={"handhandle_httpstatus_list": [404]})#, 'proxy': 'http://scraperapi:7cffa506b29e6c89d14c80bd13083a1c@proxy-server.scraperapi.com:8001'})

    def parse_pages(self, response):
        splash_args = {'timeout': 85, 'wait': 2.5}
        aircrafts = response.xpath('//a[text()="View Details"]/@href').extract()
        
        for aircraft in aircrafts:
            aircraftsItem = AircraftsItem()
            aircraftsItem['source'] = "https://www.globalair.com"+aircraft
            yield SplashRequest(url="https://www.globalair.com"+aircraft, callback=self.parse, args=splash_args, dont_filter=True, meta={"aircraftsItem": aircraftsItem})# 'proxy': 'http://scraperapi:7cffa506b29e6c89d14c80bd13083a1c@proxy-server.scraperapi.com:8001'})
            
        
       
    
            
    def parse(self, response):
        aircraftsItem = response.meta.get('aircraftsItem')        
        infos = response.css('.breadcrumb-item a::text').extract()
        if len(infos) > 1:
            make = infos[-2]
            model = infos[-1]
            aircraftsItem['make'] = make
            aircraftsItem['model'] = model

        data = response.css('.col-md-6 div::text').extract()
        if len(data) > 24:
            year = data[6]
            location = data[11]
            time = data[24]
            inf = response.css('.col-md-6 a::text').extract()
            serial_number = inf[1]
            price = response.css('#header-price::text').extract_first().replace('Price:', '')
            dealer = inf[0]
            
            aircraftsItem['year'] = year
            aircraftsItem['time'] = time
            aircraftsItem['serial_Number'] = serial_number
            aircraftsItem['price'] = price
            aircraftsItem['dealer'] = dealer
            aircraftsItem['location'] = location
        

        yield aircraftsItem

        