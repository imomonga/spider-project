# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymysql import *

class BeikeMysqlPipeline(object):
    def __init__(self):
        dbparams = {
            'host': '192.168.231.132',
            'port': 3306,
            'user': 'root',
            'password': 'zkwsud888',
            'database': 'beike',
            'charset': 'utf8',
        }
        self.conn = connect(**dbparams)
        self.cursor = self.conn.cursor()
        self._sql = None

    def process_item(self, item, spider):
        self.cursor.execute(self.sql, (item['province'], item['city'],
                                       item['name'], item['area'], item['rooms'], item['price'], item['time'],
                                       item['origin_url']))
        self.conn.commit()
        return item

    @property
    def sql(self):
        if not self._sql:
            self._sql = """
                            insert into beike(id,province,city,name,area,rooms,price,time,origin_url) values(Null,%s,%s,%s,%s,%s,%s,%s,%s)
                        """

            return self._sql
        return self._sql




import json

class BeikePipeline(object):
    def __init__(self):
        self.file = open('zufang','wb')
    def process_item(self, item, spider):
        content = json.dumps(dict(item), ensure_ascii=False).encode("utf-8")+b"\n"
        self.file.write(content)
        return item
    def close_spider(self,spider):
        self.file.close()
#
#
#
#
# import pymysql
# from twisted.enterprise import adbapi
# from pymysql import cursors
#
#
# class BeiKeTwistedPipeline(object):
#     def __init__(self):
#         #password = input("请输入mysql密码")
#         dbparams = {
#             'host': '127.0.0.1',
#             'port': 3306,
#             'user': 'root',
#             'password': 'zkwsud888',
#             'database': 'beike',
#             'charset': 'utf8',
#             'cursorclass': cursors.DictCursor
#         }
#
#         self.dbpool = adbapi.ConnectionPool("pymysql", **dbparams)
#         self._sql = None
#
#     @property
#     def sql(self):
#         if not self._sql:
#             self._sql = """
#                             insert into beike(id,province,city,name,area,rooms,
#                             price,time,origin_url) values(null,%s,%s,%s,%s,%s,%s,%s,%s)
#                         """
#             return self._sql
#         return self._sql
#
#     def process_item(self, item, spider):
#         defer = self.dbpool.runInteraction(self.insert_item, item)
#         defer.addErrback(self.handle_error, item, spider)
#
#     def insert_item(self, cursor, item):
#         cursor.execute(self.sql, (item['province'], item['city'],
#                                        item['name'], item['area'], item['rooms'], item['price'],item['time'],
#                                        item['origin_url']))
#
#     def handle_error(self, error, item, spider):
#         # print(error)
#         pass


# import json

#1.手动把dick转换成json格式

# class QsbkPipeline(object):
#     def __init__(self):
#         self.fp = open('duanzi.json','w',encoding='utf-8')
#
#     def open_spider(self,spider):
#         print('开始爬虫')
#
#     def process_item(self, item, spider):
#         item_json = json.dumps(dict(item),ensure_ascii=False)
#         self.fp.write(item_json+'\n')
#         return item
#
#     def close_spider(self,spider):
#         self.fp.close()
#         print('爬虫结束了')

#2.适用JsonItemExporter，使用与数据量小的情况下
# from scrapy.exporters import JsonItemExporter
# class QsbkPipeline(object):
#     def __init__(self):
#         self.fp = open('duanzi.json','wb')
#         self.exporter = JsonItemExporter(self.fp,ensure_ascii=False,encoding='utf-8')
#         self.exporter.start_exporting()
#
#     def open_spider(self,spider):
#         print('开始爬虫')
#
#     def process_item(self, item, spider):
#         self.exporter.export_item(item)
#         return item
#
#     def close_spider(self,spider):
#         self.exporter.finish_exporting()
#         self.fp.close()
#         print('爬虫结束了')


# 3.JsonLinesItemExporter，适用与数据量大的情况下
# from scrapy.exporters import JsonLinesItemExporter
# class QsbkPipeline(object):
#     def __init__(self):
#         self.fp = open('duanzi.json','wb')
#         self.exporter = JsonLinesItemExporter(self.fp,ensure_ascii=False,encoding='utf-8')
#
#     def open_spider(self,spider):
#         print('开始爬虫')
#
#     def process_item(self, item, spider):
#         self.exporter.export_item(item)
#         return item
#
#     def close_spider(self,spider):
#         self.fp.close()
#         print('爬虫结束了')



# import os
# from urllib import request
#
# class BmwPipeline(object):
#     def __init__(self):
#         self.path = os.path.join(os.path.dirname(__file__),"images")
#         if not os.path.exists(self.path):
#             os.mkdir(self.path)
#
#     def process_item(self, item, spider):
#         partname = item['partname']
#         urls = item['urls']
#         partpath = os.path.join(self.path,partname)
#         if not os.path.exists(partpath):
#             os.mkdir(partpath)
#         for url in urls:
#             imagename = url.split('__')[-1]
#             request.urlretrieve(url,os.path.join(self.path,imagename))
#         return item
