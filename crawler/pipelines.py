# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json


class ContentPipeline(object):
    results = []
    def process_item(self, item, spider):
        self.results.append(dict(item))
        return item

    def open_spider(self, spider):
        self.results = []

    def close_spider(self, spider):
        if spider.name in ['content', 'search', 'update']:
            print(json.dumps(self.results))
