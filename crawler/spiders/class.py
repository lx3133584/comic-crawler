import scrapy
import re
from crawler.items import ClassItem
from crawler.utils import exportOne
from config import baseUrl

class ClassSpider(scrapy.spiders.Spider):
    name = "class"
    start_urls = [baseUrl]

    def parse(self, response):
        for class_url in response.xpath("//div[@class='cHNav']//span/a/@href").extract():
            url = self.start_urls[0] + class_url
            yield scrapy.Request(url, callback=self.class_parse)

    def class_parse(self, response):
        num = exportOne(response.xpath("//div[@id='iComicPC1']//b[last()]/text()").extract())
        start_url = self.start_urls[0]
        cur_class_id = re.search(r'\d+', response.url).group(0)
        for index in range(int(num)):
            url = start_url + 'comic/class_' + cur_class_id + '/%d.html' % index
            yield scrapy.Request(url, callback=self.item_parse)

    def item_parse(self, response):
        list = response.xpath("//div[@id='list']")
        class_name = exportOne(list.xpath("div[@class='cMBR_Title']/text()[last()]").extract()).strip()
        for li in response.xpath("//div[@class='cComicList']/li"):
            item = ClassItem()
            item['name'] = exportOne(li.xpath('a/@title').extract())
            item['class_name'] = class_name
            id = re.search(r'\d+', exportOne(li.xpath('a/@href').extract())).group(0)
            item['id'] = int(id)
            yield item
