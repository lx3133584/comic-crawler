import scrapy
import json
import re
from crawler.items import DetailItem
from crawler.utils import exportOne
from config import baseUrl

class DetailSpider(scrapy.spiders.Spider):
    name = "detail"
    start_urls = ["%s/manhua" % baseUrl]

    def __init__(self, id=3390, *args, **kwargs):
        super(DetailSpider, self).__init__(*args, **kwargs)
        self.start_urls = ["%s/manhua/%d.html" % (baseUrl, int(id))]

    def parse(self, response):
        detail = DetailItem()
        body = response.xpath("//div[@id='permalink']")

        detail['cover'] = exportOne(body.xpath("div[@id='about_style']/img/@src").extract())
        about_kit = body.xpath("div[@id='about_kit']/ul")
        detail['title'] = exportOne(about_kit.xpath("li[1]/h1/text()").extract()).strip()
        detail['author'] = exportOne(about_kit.xpath("li[2]/text()").extract())
        detail['status'] = exportOne(about_kit.xpath("li[3]/text()").extract())
        detail['update_time'] = exportOne(about_kit.xpath("li[5]/text()").extract())
        desc = exportOne(about_kit.xpath("li[8]/text()").extract())
        detail['desc'] = desc.replace(':', '')
        popularity_number = exportOne(about_kit.xpath("li[4]/text()").extract())
        popularity_number = re.search(r'\(\d+\)', popularity_number).group(0)
        popularity_number = re.search(r'\d+', popularity_number).group(0)
        detail['popularity_number'] = int(popularity_number)
        collection_number = exportOne(about_kit.xpath("li[6]/text()").extract())
        collection_number = re.search(r'\d+', collection_number).group(0)
        detail['collection_number'] = int(collection_number)
        score_number = exportOne(about_kit.xpath("li[7]/text()").extract())
        score_number = re.search(r'\d+', score_number).group(0)
        detail['score_number'] = int(score_number)
        score = exportOne(about_kit.xpath("li[7]/span[1]/text()").extract())
        detail['score'] = float(score)

        List = []
        for outer_list in body.xpath("div[@class='cVolList']/ul"):
            outer = {}
            outer['category_name'] = exportOne(outer_list.xpath('preceding-sibling::div[1]/text()').extract())
            outer['list'] = []
            for inner_list in outer_list.xpath('li'):
                inner = {}
                inner['title'] = exportOne(inner_list.xpath('a/@title').extract())
                inner['link'] = exportOne(inner_list.xpath('a/@href').extract()).replace('/page', '').replace('/cool', '')
                outer['list'].append(inner)
            List.append(outer)
        result = {'detail': dict(detail), 'list': List}
        print(json.dumps(result))
