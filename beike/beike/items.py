# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
class BeikeItem(scrapy.Item):
    province = scrapy.Field()
    city = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    area = scrapy.Field()
    rooms = scrapy.Field()
    time = scrapy.Field()
    origin_url = scrapy.Field()


