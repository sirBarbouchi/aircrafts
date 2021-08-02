import scrapy
from scrapy_splash import SplashRequest
from ..items import AircraftsItem

def listToString(l):
    s = ''
    for e in l:
        s += e + " "
    return s.replace('Upgraded', '')
class GulfstreamSpider(scrapy.Spider):
    name = 'gulfstream'
    
    
    def start_requests(self):
        url = "https://www.gulfstream.com/en/pre-owned/"
        splash_args = {'timeout': 85, 'wait': 0.5}

        yield SplashRequest(url=url, callback=self.parse, args=splash_args, meta={"handhandle_httpstatus_list": [404]})#, 'proxy': 'http://scraperapi:7cffa506b29e6c89d14c80bd13083a1c@proxy-server.scraperapi.com:8001'})

    def parse(self, response):
        
        aircrafts = response.css('.preowned__stats')
        print("**************")
        print(len(aircrafts))
        for aircraft in aircrafts:
            source = "https://https://www.gulfstream.com/en/pre-owned/"
            
            year = aircraft.css('h4::text').extract_first().replace('Model Year: ', '')
            info = aircraft.css('h2::text').extract_first().split('S/N')
            serial_number = info[-1].strip()
            make = listToString(info[0].strip().split(' ')[:-1])
            model = info[0].strip().split(' ')[-1]
            time = aircraft.css('p::text').extract()[2].replace('Total time:', '').replace('hours', '').strip()
            price = aircraft.css('p::text').extract()[-1].replace('Asking price: ', '')
            print("model", model)
            print("make", make)
            print("serial", serial_number)
            print('time', time)
            print('price', price)
                       
            aircraftsItem = AircraftsItem()
            aircraftsItem['source'] = source
            aircraftsItem['make'] = make
            aircraftsItem['model'] = model
            aircraftsItem['year'] = year
            aircraftsItem['time'] = time
            aircraftsItem['serial_Number'] = serial_number
            aircraftsItem['price'] = price
            aircraftsItem['dealer'] = "gulfstream"

            yield aircraftsItem

    
