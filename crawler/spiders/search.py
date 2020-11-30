import scrapy
import re
from crawler.items import SearchItem
from crawler.utils import exportOne
from config import baseUrl

class SearchSpider(scrapy.spiders.Spider):
    name = "search"
    start_urls = ["%s/comic/?act=search&st=" % baseUrl]

    def __init__(self, keyword='', *args, **kwargs):
        super(SearchSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['%s/comic/?act=search&st=%s' % (baseUrl, keyword)]

    def parse(self, response):
        for li in response.xpath("//div[@id='list']/div[2]/li"):
            item = SearchItem()
            item['title'] = exportOne(li.xpath('a/@title').extract())
            id = re.search(r'\d+', exportOne(li.xpath('a/@href').extract())).group(0)
            item['id'] = int(id)
            item['cover'] = exportOne(li.xpath('a/img/@src').extract())
            yield item
