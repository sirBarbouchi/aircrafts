import scrapy
from scrapy_splash import SplashRequest
from ..items import AircraftsItem
class DassaultSpider(scrapy.Spider):
    name = 'dassault'
    
    
    def start_requests(self):
        url = "https://www.dassaultfalcon.com/en/Aircraft/PreOwned/Pages/Pre-owned_list.aspx"
        splash_args = {'timeout': 85, 'wait': 0.5}

        yield SplashRequest(url=url, callback=self.parse, args=splash_args)

    def parse(self, response):
        
        aircrafts = response.css('.preowned-item')
        print("**************")
        for aircraft in aircrafts:
            link = aircraft.css('a').xpath('@href').extract_first()
            model = aircraft.css('h3::text').extract_first()
            informations = aircraft.css('li::text').extract()

            print(link)
            
            aircraftsItem = AircraftsItem()
            aircraftsItem['source'] = link
            aircraftsItem['make'] = "Dassault"
            aircraftsItem['model'] = model
            aircraftsItem['year'] = informations[0]
            aircraftsItem['serial_Number'] = informations[1]
            aircraftsItem['price'] = informations[2]
            aircraftsItem['dealer'] = "Dassault"

            yield scrapy.Request(url=link, callback=self.parse_aircraft, meta={'aircraftsItem': aircraftsItem})

    def parse_aircraft(self, response):
        
        
        print("*********")
        time = response.css('td::text').extract()[1]
        aircraftsItem = response.meta.get('aircraftsItem')
        aircraftsItem['time'] = time
        yield aircraftsItem

