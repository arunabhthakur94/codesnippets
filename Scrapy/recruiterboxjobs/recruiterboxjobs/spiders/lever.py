import scrapy
from bs4 import BeautifulSoup
import html.parser
from scrapy.utils.response import open_in_browser
from scrapy.selector import Selector
from ..items import RecruiterboxjobsItem

class CrawlLever(scrapy.Spider):
    name = "lever"
    start_urls = [
        'https://www.google.com/search?&q=site:lever.co'
    ]

    page_number = 1
    inner_pages = 0
    page_count = 0

    def parse(self, response):
        html_source = response.body
        html = BeautifulSoup(html_source, 'html.parser')
        with open('/tmp/HTML/lever/page' + str(CrawlLever.page_number) + '.html', 'w', encoding='utf-8') as f:
            f.write(str(html.prettify()))
        
        next_page = response.xpath('/html/body/div/footer/div[1]/div/div/a/@href').extract_first()

        internal_pages = response.css('a::attr(href)').extract()
        for i in internal_pages:
            url_start = i[0:5]
            if url_start == '/url?':
                inner_url = "https://www.google.com"+i
                yield response.follow(inner_url, callback = self.parseUrl)

        if next_page is not None and CrawlLever.page_number < 32:
            CrawlLever.page_count += 10
            CrawlLever.page_number += 1
            go_next = 'https://www.google.com/search?q=site:lever.co&start='+str(CrawlLever.page_count)
            yield response.follow(go_next, callback = self.parse)

    # LEVEL-2 CRAWLING

    def parseUrl(self, response):
        # open_in_browser(response)
        CrawlLever.inner_pages += 1
        html_source = response.body
        html = BeautifulSoup(html_source, 'html.parser')
        with open ('/tmp/HTML/Level-2/innerpage'+str(CrawlLever.inner_pages)+'.html', 'w', encoding='utf-8') as f:
            f.write(str(html.prettify()))

