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
from scrapy.pipelines.files import FilesPipeline
from scrapy.pipelines.files import GCSFilesStore


class GCSFilesStoreJSON(GCSFilesStore):
    CREDENTIALS = {
  "type": "service_account",
  "project_id": "my-scrapy-project-45354",
  "private_key_id": "049039995ed79b996004910f1eb2d310e334f7ed",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDcaoFLSMhWYGuu\n3nqkVwRlUoTXVW0QgB5DTeVrJSAYnpUcd3yTrxQKaw22Y4RK5mlY2XAvDtb9l9y/\nqyMVT4MbZpRvftm1cDnnxHJy8GNZhBJk33o9TjY+16HuvjoNsTo68P09bGxenTxQ\nTCVuXpAMPOHKHTAHsc7TexqNrHRdSYDSBSQlu5NR5suX4mpZ13hSzANBZcsaAdAh\ns03LZs2ECiRkg7q8XLrwLhC9wBrf12JZmz/Or2cUpEkfBeT3ftOGA7YsvQEncU8z\n5KwT6kFQ7f/5+G1G+wscjtYtN7ItZVHad6f3XBbdQpnlAhw6QMAW4NYddXHuT8lX\naM0tD4P5AgMBAAECggEAEQ4QqRGdpslZK7O9S6AMEAb9jmfmw4MWVGDfopXB0QXc\nRdKdChRe+Ztk+TrkDqObfSt9+bYtPnwUsaP9V/XKEEG0tJfdIqPnZx6VOH2PQmrs\nvW9pVvsJSX2H4yBG/6458juZbLpJ/FwwQYpSzyJ0BO5lDi2J/N5uQYDiAhpY+qrD\nf3Sb7FohpybSUJL/2XcNfcjJmyWbSEfNFzQ0EpA89JFBNPgC0YV6+1/s2WHrzMcX\nWkxDHRqnnm4ab3pS2iS/VoRZRtcP7BUnO4I2ylwv6/h2H+/1tqT/weOoFkNuI5OL\nFpZR0oT6a8bR1hSgTVgc1yQtN+X/o544RoKI/WnD3QKBgQD8l3hDWDeNR8sCeS8E\nU0KGXYFQz0YWeUzpbvHXqlEJrgxX9reN1zEFB0kqPl18rJifWwfp3Tyyjk39DFje\ni+rOT6h0oagoWCr2nr+vqFvN9DSeCUmxQu2NHLYRrNuX/99oSL3Wz9w3URWcGBcp\n7bo0N3mIQMtYbz5PHKpKrVMwiwKBgQDfY+P+L5oIs2ewUA6zfm8I1dOjWso3SKjq\n/TQYPgvx79QCiRkSakeaM6oTg1WidLovtylM41/9awos5UDSs7A3VChHSfDqOBLw\nM1YKX/83OpQFLrjZQ/qXWPqkmaAvButmgigNL9bb0v3PKLkmmdhE7lh+kwyQp+qP\nci8ps6UKCwKBgDoOOmcIJKSFRsTHw6Wz2Ut2vF0tdsd9k87nYBCYpc2awl2JaEDi\nn/Ku7QMXmHcqWF3wF06KOgQ0LvqlVtu3vv0yU96StUqokR9j91zRTmB0648TRWvH\nnT/cxIAlgcda2Sdn6LIxzkSsj1H0O4a4jB6qTXWiptopn2GhjgZh9gfnAoGBANyS\nPx5OViNdMXaPtdRZdL0elJfpH12y6scMOBHvwc+jZI0UXaMnOYfyl24o8bc01loi\n2i7HG5KXzDZELttc/RPEjvjE85HwyBJQPhaEbvVTa7AqT+6HBrnF68X2wolspaZT\nwcQzhk0LafzQUvDgWwDE7rAb9f4nLp1wu0zLypu9AoGBALhPhDVdq7EHLjIKiEjq\nxfbTMwWfCc7RGxiqVjjIubWu23Jx8/zHTjFLBXFnEPjr7quTOOzJfouQTJ8lhmbr\nKYprnBUwPA9uBt1xpmYHnmw7DNDn3dcyJLw7nL/My3oed1cBhdmI83jta8Ajk+ms\n4QdfKH0L60GVdQ6LBYIZ/dyK\n-----END PRIVATE KEY-----\n",
  "client_email": "quotes@my-scrapy-project-45354.iam.gserviceaccount.com",
  "client_id": "109295532592901413450",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/quotes%40my-scrapy-project-45354.iam.gserviceaccount.com"
}

def __init__(self, uri):
    try:
        from google.cloud import storage
    except ImportError:
        from google.datalab import storage
    client = storage.Client.from_service_account_info(self.CREDENTIALS)
    bucket, prefix = uri[5:].split('/', 1)
    self.bucket = client.bucket(bucket)
    self.prefix = prefix

class GCSFilePipeline(FilesPipeline):
    def __init__(self, store_uri, download_func=None, settings=None):
        super(GCSFilePipeline, self).__init__(store_uri,download_func,settings)

class TutorialPipeline(object):
    def process_item(self, item, spider):
        return item

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
    # pass
