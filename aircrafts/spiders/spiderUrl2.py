import scrapy
from scrapy_splash import SplashRequest
from ..items import AircraftsItem
from scrapy.http import Request
import requests
import json



class ControllerSpider(scrapy.Spider):
    name = 'controller'
        
    def start_requests(self):
        
        url = "https://www.controller.com/ajax/listings/ajaxsearch?Category=3&ScopeCategoryIDs=13&sort=1&page="
        splash_args = {'timeout': 85, 'wait': 2.5}
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        response = requests.get('https://www.controller.com/ajax/listings/ajaxsearch?Category=3&ScopeCategoryIDs=13&sort=1&page=')
  
        # prinitng request content
        n = response.json().get('ListingsCount')
        n_pages = n // 25 + 1
        for page in range(1, n_pages+1):
            yield scrapy.Request(url=url+str(page), callback=self.parse_pages)#, args=splash_args, dont_filter=True, meta={"handhandle_httpstatus_list": [404]}, headers=headers)

    def parse_pages(self, response):
        splash_args = {'timeout': 85, 'wait': 2.5}

        aircrafts = json.loads(response.body).get('Listings')


        for aircraft in aircrafts:
            make = aircraft.get('ManufacturerName').strip()
            model = aircraft.get('Model')
            source = 'https://www.controller.com/' + aircraft.get('DetailUrl')
            price = aircraft.get('RetailPrice')
            dealer = aircraft.get('Dealer')
            serial_number = aircraft.get('SerialNumber')
            location = aircraft.get('DealerLocation')
            year = aircraft.get('ListingTitle').split(make)[0]
            specs = aircraft.get('Specs')
            time = None
            for spec in specs:
                if spec.get("Key") == "Total Time":
                    time = spec.get('Value')
                    break
            aircraftsItem = AircraftsItem()
            aircraftsItem['source'] = source
            aircraftsItem['make'] = make
            aircraftsItem['model'] = model
            aircraftsItem['year'] = year
            aircraftsItem['serial_Number'] = serial_number
            aircraftsItem['price'] = price
            aircraftsItem['dealer'] = dealer
            aircraftsItem['time'] = time
            aircraftsItem['location'] = location
            yield aircraftsItem
