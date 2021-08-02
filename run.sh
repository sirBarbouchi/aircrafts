#!/bin/bash

rm aircrafts.csv
scrapy crawl avbuyer -o aircrafts.csv
scrapy crawl jamesedition -o aircrafts.csv
scrapy crawl jetcraft -o aircrafts.csv
scrapy crawl globalair -o aircrafts.csv
scrapy crawl tradeAplane -o aircrafts.csv
scrapy crawl gulfstream -o aircrafts.csv
scrapy crawl bombardier -o aircrafts.csv
scrapy crawl txtav -o aircrafts.csv
scrapy crawl businessair -o aircrafts.csv
scrapy crawl dassault -o aircrafts.csv
