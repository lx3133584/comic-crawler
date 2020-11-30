import scrapy
import re
from crawler.items import AllItem
from crawler.utils import exportOne
from config import baseUrl

class AllSpider(scrapy.spiders.Spider):
    name = "all"
    start_urls = ["%s/comic/1.html" % baseUrl]

    def item_parse(self, response):
        for li in response.xpath("//div[@class='cComicList']/li"):
            item = AllItem()
            item['name'] = exportOne(li.xpath('a/@title').extract())
            id = re.search(r'\d+', exportOne(li.xpath('a/@href').extract())).group(0)
            item['id'] = int(id)
            yield item

    def parse(self, response):
        start_url = self.start_urls[0]
        for index in range(1128):
            url = re.sub(r'\/\d\.html', '/%d.html' % (index + 1), start_url)
            yield scrapy.Request(url, callback=self.item_parse)
