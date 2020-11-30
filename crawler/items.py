# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SearchItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    cover = scrapy.Field()

class DetailItem(scrapy.Item):
    author = scrapy.Field()
    title = scrapy.Field()
    cover = scrapy.Field()
    status = scrapy.Field()
    update_time = scrapy.Field()
    desc = scrapy.Field()
    popularity_number = scrapy.Field()
    collection_number = scrapy.Field()
    score_number = scrapy.Field()
    score = scrapy.Field()

class ContentItem(scrapy.Item):
    index = scrapy.Field()
    url = scrapy.Field()

class AllItem(scrapy.Item):
    name = scrapy.Field()
    id = scrapy.Field()

class ClassItem(scrapy.Item):
    name = scrapy.Field()
    class_name = scrapy.Field()
    id = scrapy.Field()

class UpdateItem(scrapy.Item):
    update_time = scrapy.Field()
    id = scrapy.Field()
