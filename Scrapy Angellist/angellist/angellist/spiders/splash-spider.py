from scrapy.spiders import Spider
from ..items import GameItem

class MySpider(Spider):
    name = 'SplashSpider'
    start_urls = [
        'https://www.livescore.bet3000.com'
    ]

    def parse(self, response):
        item = GameItem()
        
        return item
