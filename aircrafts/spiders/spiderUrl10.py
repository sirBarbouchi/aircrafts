import scrapy
from scrapy_splash import SplashRequest
from ..items import AircraftsItem

def listToString(l):
    s = ''
    for e in l:
        s += e
    return s.replace('Upgraded', '')
class TxtavSpider(scrapy.Spider):
    name = 'txtav'
    
    
    def start_requests(self):
        url = "https://txtav.com/en/preowned"
        splash_args = {'timeout': 85, 'wait': 2.5}

        yield SplashRequest(url=url, callback=self.parse, args=splash_args)

    def parse(self, response):
       
        aircrafts = response.css('.listing-wrapper')
        print("**************")
        print(len(aircrafts))
        for aircraft in aircrafts:
            href = aircraft.css('.more a').xpath('@href').extract_first()
            if href:
                source = "https://txtav.com" + href
            info = aircraft.css('h3::text').extract_first().split('-')[-1].strip().split(' ')
            aircraftsItem = AircraftsItem()

            if len(info) > 1:
                year = info[0]
                model = info[-1]
                make = listToString(info[1:-1])
                aircraftsItem['make'] = make
                aircraftsItem['model'] = model
                aircraftsItem['year'] = year
            serial_number = aircraft.css('strong.ng-binding::text').extract_first()
            time = aircraft.css('span.ng-binding::text').extract_first().replace('hours', '')
           
           
            aircraftsItem['source'] = source
            
            aircraftsItem['time'] = time
            aircraftsItem['serial_Number'] = serial_number
            aircraftsItem['dealer'] = "Textron Aviation"

            yield aircraftsItem

    
