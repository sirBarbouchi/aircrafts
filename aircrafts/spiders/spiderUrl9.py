import scrapy
from scrapy_splash import SplashRequest
from ..items import AircraftsItem

def listToString(l):
    s = ''
    for e in l:
        s += e + " "
    return s.replace('Upgraded', '')
class BombardierSpider(scrapy.Spider):
    name = 'bombardier'
    
    
    def start_requests(self):
        url = "https://businessaircraft.bombardier.com/en/aircraft/pre-owned"
        splash_args = {'timeout': 85, 'wait': 0.5}

        yield SplashRequest(url=url, callback=self.parse, args=splash_args)

    def parse(self, response):
        
        aircrafts = response.css('.bba-stack-withspacing li')
        print("**************")
        for aircraft in aircrafts:
            source = "https://businessaircraft.bombardier.com" + aircraft.css('.bba-preowned-list-item-ctas a').xpath('@href').extract_first()
            
            info = aircraft.css('div.bba-preowned-list-item-title::text').extract_first().split('S/N')
            serial_number = info[-1].strip()
            make = listToString(info[0].strip().split(' ')[:-1])
            model = info[0].strip().split(' ')[-1]
           
            year = aircraft.css('div.bba-preowned-list-item-specs-item span::text').extract_first()
            time = aircraft.css('div.bba-preowned-list-item-specs-item span::text').extract()[2].replace('Hours', '')
            
           
            aircraftsItem = AircraftsItem()
            aircraftsItem['source'] = source
            aircraftsItem['make'] = make
            aircraftsItem['model'] = model
            aircraftsItem['year'] = year
            aircraftsItem['time'] = time
            aircraftsItem['serial_Number'] = serial_number
            aircraftsItem['dealer'] = "bombardier"

            yield aircraftsItem

    
