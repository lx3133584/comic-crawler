import scrapy
import json
import re
from crawler.items import UpdateItem
from crawler.utils import exportOne
from config import baseUrl

class UpdateSpider(scrapy.spiders.Spider):
    name = "update"
    start_urls = ["%s/top/newrating.aspx" % baseUrl]

    def parse(self, response):
        for li in response.xpath("//div[@id='list']/div[@class='cTopComicList']/div[@class='cComicItem']"):
            item = UpdateItem()
            id = re.search(r'\d+', exportOne(li.xpath('a/@href').extract())).group(0)
            item['id'] = int(id)
            update_time = re.sub(r'[^\d\s:/]', '', exportOne(li.xpath("span[@class='cComicRating']/text()").extract()))
            item['update_time'] = update_time
            yield item
