# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MovieItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()  # 电影名
    score = scrapy.Field()  # 评分
    motto = scrapy.Field()  # 座右铭
    # actor = scrapy.Field()  # 演员
    # classification = scrapy.Field()  # 分类，级别
    # year = scrapy.Field()  # 年份
    # director = scrapy.Field()  # 导演

