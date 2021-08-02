import scrapy
from scrapy_splash import SplashRequest
from ..items import AircraftsItem
from scrapy.http import Request

import json

class JetcraftSpider(scrapy.Spider):
    name = 'jetcraft'
        
    def start_requests(self):
        url = "https://www.jetcraft.com/aircraft/?order_by=date&order=DESC#038;order=DESC"
        splash_args = {'timeout': 85, 'wait': 2.5}

        yield SplashRequest(url=url, callback=self.parse_pages, args=splash_args, dont_filter=True)

    def parse_pages(self, response):
        splash_args = {'timeout': 85, 'wait': 2.5}
        #aircrafts = response.xpath('//a[text()="View Details"]/@href').extract()
        aircrafts = response.css('.aircraft')
        
        for aircraft in aircrafts:

            source = aircraft.css('a').xpath('@href').extract_first()
            year = source.split('/')[-3]
            model = source.split('/')[-4]
            make = source.split('/')[-5]
            serial_number = source.split('/')[-2].split('-s-n-')[-1]
            info = aircraft.css('li::text').extract_first()
            time = info.split('Hours;')[0].strip()
            print(f'time {time}')
            print('year ', year)
            print('make ', make)
            print(f'model {model}')
            print(f'serial number {serial_number}')
            aircraftsItem = AircraftsItem()
            aircraftsItem['year'] = year
            aircraftsItem['time'] = time
            aircraftsItem['serial_Number'] = serial_number
            aircraftsItem['dealer'] = 'jetcraft'
            aircraftsItem['make'] = make
            aircraftsItem['model'] = model
            aircraftsItem['source'] = source
            yield aircraftsItem
            
        
        href = response.xpath('//a[span//text()="Next"]/@href').extract_first()
        if href:
            yield SplashRequest(url=href, callback=self.parse_pages, args=splash_args, dont_filter=True)
    
    
            
    
        