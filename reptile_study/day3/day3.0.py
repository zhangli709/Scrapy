
import pymongo


def main():
    # client = pymongo.MongoClient('mongodb://47.106.171.59:27017')
    client = pymongo.MongoClient(host='47.106.171.59', port=27017)
    # client = pymongo.MongoClient(host='120.77.222.217', port=27017)
    db = client.teacherluo
    pages_cache = db.foo
    # 一个花括号，就是一个文档  增
    # page_id = pages_cache.insert_one({'url':'http://www.baidu.com', 'content': 'shit'})
    # content = pages_cache.insert_many([
    #     {'name': 'foo1', 'addr': '成都'},
    #     {'name': 'foo2', 'addr': '千锋'},
    #     {'name': 'foo3', 'addr': '力保'}])

    # 改
    pages_cache.update({'_id': 5}, {'$set': {'1': '在', '2': '都是'}}, upsert=True)
    # print(content)

    # 查
    # print(pages_cache.find_one({'_id': 5}))
    # for i in pages_cache.find():
    #     print(i)

    # 删
    # pages_cache.remove({'name': 'foo3'})


if __name__ == '__main__':
    main()