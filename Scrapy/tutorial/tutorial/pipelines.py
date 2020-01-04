# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# Scraped data -> Item Container -> JSON/CSV file
# Scraped data -> Item Container -> pipeline -> DB

import MySQLdb
import sys
import hashlib
from scrapy.exceptions import DropItem
from scrapy.http import Request


class TutorialPipeline(object):
    # def __init__(self):
    #     self.conn = MySQLdb.connect('localhost','root','','practise', charset="utf8",use_unicode=True)
    #     self.cursor = self.conn.cursor()

    # def process_item(self, item, spider):
    #     try:
    #         self.cursor.execute("""insert into quotes (title, author, tags) values (%s, %s, %s)""",(
    #             item['title'][0].encode('utf8'),
    #             item['author'][0].encode('utf8'),
    #             item['tag'][0].encode('utf8')
    #             )
    #         )
    #         self.conn.commit()
    #     except:
    #         return item
    pass
