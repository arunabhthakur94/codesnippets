import MySQLdb
import sys
import hashlib
from scrapy.exceptions import DropItem
from scrapy.http import Request

class MySQLStorePipelile(object):
    def __init__(self):
        self.conn = MySQLdb.connect('localhost:3306','root','','practise', charset="utf-8",use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        try:
            self.cursor.execute("""insert into quotes values (%s,%s,%s)""",item['title'].encode('utf-8'),item['author'].encode('utf-8'),item['tags'].encode('utf-8'))
            self.conn.commit()
            self.conn.close()
            print("Done")
        except:
            print("Not Connected")
            return item