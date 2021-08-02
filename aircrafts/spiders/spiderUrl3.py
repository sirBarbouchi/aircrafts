import scrapy
from scrapy_splash import SplashRequest
from ..items import AircraftsItem
from scrapy.http import Request

import json
def process(l):
    d = {}
    for i in range(0, len(l), 2):
        d[l[i].strip()] = l[i+1].strip()
    return d


class JameseditionSpider(scrapy.Spider):
    name = 'jamesedition'
        
    def start_requests(self):
        url = "https://www.jamesedition.com/jets?order=premium"
        splash_args = {'timeout': 85, 'wait': 2.5}

        yield SplashRequest(url=url, callback=self.parse_pages, args=splash_args, dont_filter=True)

    def parse_pages(self, response):
        splash_args = {'timeout': 85, 'wait': 2.5}
        aircrafts = response.css('.JE-search-results__grid-item')
        for aircraft in aircrafts:
            href = aircraft.css('.JE-search-result__link').xpath('@href').extract_first()
            print("href ", href)
            if href:
                source = "https://www.jamesedition.com" + href
                make = href.split('/')[2]
                model = href.split('/')[3]
                aircraftsItem = AircraftsItem()
                
                aircraftsItem['dealer'] = 'jetcraft'
                aircraftsItem['make'] = make
                aircraftsItem['model'] = model
                aircraftsItem['source'] = source
                yield SplashRequest(url=source, callback=self.parse_page, args=splash_args, dont_filter=True, meta={'aircraftsItem': aircraftsItem})
                
            
        
        href = response.css('.JE-pagination li')[4].css('a::attr(href)').extract_first()
        if href:
            yield SplashRequest(url="https://www.jamesedition.com"+href, callback=self.parse_pages, args=splash_args, dont_filter=True)
        
    
            
    def parse_page(self, response):
        price = response.css('.price::text').extract_first()
        infos = response.css('.details-list')
        aircraftsItem = response.meta.get('aircraftsItem')                    
        aircraftsItem['price'] = price
        #print(json.loads(response.request.body.decode('utf8'))['url'])
        data = infos.css('span::text').extract()
        if data != []:
            data = process(data)
            if 'Year:' in data.keys():
                year = data['Year:']
                aircraftsItem['year'] = year
            if 'Location:' in data.keys():
                location = data['Location:']
                aircraftsItem['location'] = location
            if 'TTAF:' in data.keys():
                time = data['TTAF:']
                aircraftsItem['time'] = time
            if 'Serial number:' in data.keys():
                serial_number = data['Serial number:']
                aircraftsItem['serial_Number'] = serial_number
        dealer = response.css('.JE-listing-seller__title a::text').extract_first()
        aircraftsItem['dealer'] = dealer

        yield aircraftsItem

        