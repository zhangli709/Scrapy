import pymongo
import pymysql
import redis
import requests


def main():
    #获取页面
    html = requests.get('http://www.runoob.com').content.decode('utf-8')
    #找到需要的内容和链接
    client = redis.Redis(host='47.106.171.59', password=123456,port='6379')
    # client.set(key,value)
    # client.hset(kind,key,vlaue)

    conn = pymysql.connect(host='localhost', port=3306,
                           database='crawler', user='root',
                           password='123456', charset='utf8')
    cursor = conn.cursor()
    sql = ''
    cursor.executemany(sql)
    conn.commit()
    cursor.close()
    conn.close()

    client = pymongo.MongoClient(host='47.106.171.59', port='27017')
    db = client.db_name
    pages = db.tb_name
    # pages.insert_one({key,value})
    pages.insert_many({},{},{})

    # 序列化压缩
    # zipped_page = zlib.compress(pickle.dumps(html))

    # 生成摘要
    # hasher = sha1()
    # hasher.update(full_url.encode('utf-8))
    # field_key = hasher.hexdigest


if __name__ == '__main__':
    main()