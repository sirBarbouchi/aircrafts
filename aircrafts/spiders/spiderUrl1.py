import scrapy
from scrapy_splash import SplashRequest
from ..items import AircraftsItem
from scrapy.http import Request

import json

def listToString(l):
    s = ''
    for e in l:
        s += e + " "
    return s

class AvbuyerSpider(scrapy.Spider):
    name = 'avbuyer'
        
    def start_requests(self):
        
        url = "https://www.avbuyer.com/aircraft/private-jets"
        splash_args = {'timeout': 85, 'wait': 2.5}
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        yield scrapy.Request(url=url, callback=self.parse_pages)#, args=splash_args, dont_filter=True, meta={"handhandle_httpstatus_list": [404]}, headers=headers)

    def parse_pages(self, response):
        splash_args = {'timeout': 85, 'wait': 2.5}
                
        num_pages = response.css(".mb5::text").extract_first().split(" ")[5]
        num_pages = int(num_pages)//20 
        for i in range(1, num_pages+2):
             yield scrapy.Request(url="https://www.avbuyer.com/aircraft/private-jets/page-"+str(i), callback=self.parse_page)#, args=splash_args, dont_filter=True, meta={"handhandle_httpstatus_list": [404]})
        
    
    def parse_page(self, response):
        
        aircrafts = response.css('.listing-item')
        
        for aircraft in aircrafts:
            href = aircraft.css('.item-title a').xpath('@href').extract_first()
            if not href:
                make = aircraft.css('.item-title::text').extract_first().split(' ')[0]
                model = listToString(aircraft.css('.item-title::text').extract_first().split(' ')[1:])
                dealer = aircraft.css('.client-name::text').extract_first()
                price = "wanted"
                location = aircraft.css('.list-item-location::text').extract_first()
                source = response.request.url
                aircraftsItem = AircraftsItem()
                
                aircraftsItem['dealer'] = dealer
                aircraftsItem['make'] = make
                aircraftsItem['model'] = model
                aircraftsItem['source'] = source
                aircraftsItem['location'] = location
                aircraftsItem['price'] = price
                yield aircraftsItem
            
            if href:
                source = "https://www.avbuyer.com/" + href
                make = href.split('/')[3]
                model = href.split('/')[4]
                price = aircraft.css('.price::text').extract_first()
                location = aircraft.css('.list-item-location::text').extract_first().replace(', For Sale by', '').strip()
                dealer = aircraft.css('.list-item-location b::text').extract_first()
                infos = aircraft.css('.fa-no-bullet li::text').extract()
                year = infos[0].replace('Total Time', '').strip()
                serial_number = infos[1].replace('S/N ','').strip()
                time = infos[2].replace('Year','').strip()
                
                
                aircraftsItem = AircraftsItem()
                aircraftsItem['year'] = year
                aircraftsItem['time'] = time
                aircraftsItem['serial_Number'] = serial_number
                aircraftsItem['dealer'] = dealer
                aircraftsItem['make'] = make
                aircraftsItem['model'] = model
                aircraftsItem['source'] = source
                aircraftsItem['location'] = location
                aircraftsItem['price'] = price
            
                yield aircraftsItem
