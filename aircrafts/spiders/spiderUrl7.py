import scrapy
from scrapy_splash import SplashRequest
from ..items import AircraftsItem
from scrapy.http import Request

import json
def listToString(l):
    s = ''
    for e in l:
        s += e + " "
    return s.replace('Upgraded', '')
class TradeAplaneSpider(scrapy.Spider):
    name = 'tradeAplane'
    
    
    def start_requests(self):
        url = "https://www.trade-a-plane.com/search?category_level1=Jets&s-type=aircraft"
        splash_args = {'timeout': 85, 'wait': 2.5}

        yield SplashRequest(url=url, callback=self.parse_pages, args=splash_args)

    def parse_pages(self, response):
        splash_args = {'timeout': 85, 'wait': 2.5}
        this_url = "https://www.trade-a-plane.com/search?category_level1=Jets&s-type=aircraft&s-page="
        numPages = int(response.css('.search_options h2::text').extract_first().replace('\n', '').replace('\t', '').split('of')[-1].replace('results found', '').strip())
        numPages = numPages//24 + 1*(numPages%24>0)
        if numPages > 1:
            for page in range(1, numPages+1):
                print("i::::::::::::::::: ", page)
                print(this_url+str(page))
                yield SplashRequest(url=this_url+str(page), callback=self.parse_page, args=splash_args, meta={"handhandle_httpstatus_list": [404, 429]})#, 'proxy': 'http://scraperapi:7cffa506b29e6c89d14c80bd13083a1c@proxy-server.scraperapi.com:8001'})
        else:
            yield SplashRequest(url=this_url+"1", callback=self.parse_page, args=splash_args, meta={"handhandle_httpstatus_list": [404, 429]})#, 'proxy': 'http://scraperapi:7cffa506b29e6c89d14c80bd13083a1c@proxy-server.scraperapi.com:8001'})
    
    
            
    def parse_page(self, response):
        starturl = 'https://www.trade-a-plane.com'
        splash_args = {'timeout': 85, 'wait': 2.5}
        aircrafts = response.css('.result_listing')
        for aircraft in aircrafts:
            source = starturl + aircraft.css('.log_listing_click').xpath('@href').extract_first()
            year = aircraft.css('.log_listing_click::text').extract_first().strip()[:4]
            if year[0] not in ['1', '2']:
                year = None
            price = aircraft.css('.txt-price::text').extract_first().replace('\n', '').replace('\t', '')
            if not price:
                price = 'Call for Price'
            time = aircraft.css('.txt-total-time::text').extract()[1].replace('\n', '').replace('\t', '') 
            aircraftsItem = AircraftsItem()
            aircraftsItem['source'] = source
            aircraftsItem['year'] = year
            aircraftsItem['time'] = time
            aircraftsItem['price'] = price
            
            yield SplashRequest(url=source, callback=self.parse, args=splash_args, meta={'aircraftsItem': aircraftsItem,"handhandle_httpstatus_list": [429]})# 'proxy': 'http://scraperapi:7cffa506b29e6c89d14c80bd13083a1c@proxy-server.scraperapi.com:8001'}) 
        
    def parse(self, response):
         
        aircraftsItem = response.meta.get('aircraftsItem')

        infos = response.css('.info-list-seller li::text').extract()
        url = aircraftsItem['source']
        print("***************************")
        print(url)
        if infos != []:
            location = infos[-1].replace("  ", "").replace('\n', '').replace('\t', '')
            serial_number = infos[-2]
        else:
            location = None
            serial_number = None

        i = url.index("make=")
        j = url.index("&model=")
        k = url.index("&listing_id")
        make = url[i:j].replace("+", " ").replace("make=", "")
        model = url[j:k].replace("+", " ").replace("&model=", "")
        print('make ', make)
        print('model ', model)
        
        aircraftsItem['make'] = make
        aircraftsItem['model'] = model
        aircraftsItem['serial_Number'] = serial_number


        print(aircraftsItem)
        yield aircraftsItem

    
