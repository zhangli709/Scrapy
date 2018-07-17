# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os


from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline

# dd


class NbagifPipeline(object):

    def process_item(self, item, spider):
        # dir_name = dict(item)['img']
        # if not os.path.exists("E:/scrapy/nbagif/nbagif/nbagif" + dir_name):
        #     os.mkdir("E:/scrapy/nbagif/nbagif/nbagif" + dir_name)
        data = dict(item)
        for img in data:
            pic_url = data[img]
            name = pic_url[pic_url.rfind('/') + 1:]
            filename = "E:/scrapy/nbagif/nbagif/nbagif/"+ name

            try:
                with open(filename, 'a') as f:
                    from pip._vendor import requests
                    f.write(requests.get(data[img]).content)
            except IOError as e:
                print(e)
            print(name, '下载完成！')