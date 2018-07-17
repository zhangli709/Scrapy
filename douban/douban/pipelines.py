# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# 对数据的操作，存储数据
import pymongo as pymongo


class DoubanPipeline(object):

    def __init__(self):
        self.mongo_client = pymongo.MongoClient(host='47.106.171.59', port=27017)

    def process_item(self, item, spider):
        item = dict(item)  # 改成字典，放入mongo里。
        print(item)
        self.mongo_client.douban.movie.insert_one(item)
        return item
