# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
import sys
import hashlib
from scrapy.exceptions import DropItem
from scrapy.http import Request


class GoogledomainPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect('localhost','root','','practise', charset="utf8",use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        try:
            print("-------------------------------------------------------")
            self.cursor.execute("""insert into jobs (job_title, job_location, job_type, description, parent_source) values (%s, %s, %s, %s, %s)""",(
                    item['job_title'].encode('utf8'),
                    item['location'].encode('utf8'),
                    item['job_type'].encode('utf8'),
                    item['description'].encode('utf8'),
                    'RecruiterBox'
                )
            )
            self.conn.commit()
        except Exception as e:
            print('ooooooooooooooooooooooooooooooooooooooooooooooooooooooo')
            print(e)
            return item
