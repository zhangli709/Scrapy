# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from douban.items import MovieItem


class MovieSpider(scrapy.Spider):
    name = 'movie'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/top250']  # 种子url
    rules = (
        Rule(LinkExtractor(allow=(r'https://movie.douban.com/top250\?start=\d+.*'))),
        Rule(LinkExtractor(allow=(r'https://movie.douban.com/subject/\d+')), callback='parse')
    )

    def parse(self, response):
        li_list = response.xpath('//*[@id="content"]/div/div[1]/ol/li')
        for li in li_list:
            item = MovieItem()
            item['title'] = li.xpath('div/div[2]/div[1]/a/span[1]/text()').extract_first()
            item['score'] = li.xpath('div/div[2]/div[2]/div/span[2]/text()').extract_first()
            item['motto'] = li.xpath('div/div[2]/div[2]/p[2]/span/text()').extract_first()
            # item['actor'] = li.xpath().extract()
            # item['classification'] = li.xpath().extract()
            # item['year'] = li.xpath().extract()
            # item['director'] = li.xpath().extract()
            yield item  # 返回值
        # 取属性，
        href_list = response.css('a[href]::attr("href")').re('\?start=.*')
        # a_list = response.css('a[href]::text')  #  取文本
        for href in href_list:
            url = response.urljoin(href)  # 拿到新的url
            yield scrapy.Request(url=url, callback=self.parse)  # 执行完之后，回调

