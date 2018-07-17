# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from nbagif.items import NbagifItem


class BallSpider(CrawlSpider):
    name = 'ball'
    allowed_domains = ['gaoxiaogif.com']
    start_urls = ['http://www.gaoxiaogif.com/tag/lanqiu/']

    rules = (
        Rule(LinkExtractor(allow=r'http://www.gaoxiaogif.com/tag/lanqiu/index_\d+\.html'),  follow=True),
        Rule(LinkExtractor(allow=r'http://www.gaoxiaogif.com/tiyugif/'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'http://www.gaoxiaogif.com/tiyugif/\d+\.html'), callback='parse_item'),
    )

    def parse_item(self, response):
        item = NbagifItem()
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        sel = Selector(response)
        p_list = sel.xpath('/html/body/div[3]/div[2]/div[3]/div[2]/p')
        for src in p_list.xpath('img/@src').extract():
            item['img'] = src
        return item
