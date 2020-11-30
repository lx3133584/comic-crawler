import scrapy
import re
from crawler.items import ContentItem
from crawler.utils import exportOne
from config import baseUrl

def parse_img_url(name):
    s = name
    x = name[-1]
    w = "abcdefghijklmnopqrstuvwxyz"
    xi = w.find(x) + 1
    sk = s[len(s) - xi - 12 : len(s) - xi - 1]
    s = s[0 : len(s) - xi - 12]
    k = sk[0 : len(sk) - 1]
    f = sk[-1]
    for i in range(len(k)):
        s = s.replace(k[i], str(i))
    ss = s.split(f)
    s = ""
    for a in ss:
        s += chr(int(a))
    return s

class ContentSpider(scrapy.spiders.Spider):
    name = "content"
    start_urls = ["%s/cool94743/1.html?s=8" % baseUrl]

    def __init__(self, link='', *args, **kwargs):
        super(ContentSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['%s/cool%s' % (baseUrl, link)]



    def item_parse(self, response):
        item = ContentItem()
        item['index'] = int(exportOne(response.xpath("//input[@id='hdPageIndex']/@value").extract()))
        domain_data = exportOne(response.xpath("//input[@id='hdDomain']/@value").extract())
        domain = exportOne(domain_data.split("|"))
        name = exportOne(response.xpath("//div[@id='iBodyQ']//img/@name").extract())
        prefix = re.sub(r'http://[^\/]+/', '', domain)
        item['url'] = prefix + parse_img_url(name)
        return item

    def parse(self, response):
        count = int(exportOne(response.xpath("//input[@id='hdPageCount']/@value").extract()))
        start_url = self.start_urls[0]
        for index in range(count):
            url = re.sub(r'\/\d\.html', '/%d.html' % (index + 1), start_url)
            yield scrapy.Request(url, callback=self.item_parse)
