import scrapy
from bs4 import BeautifulSoup
import html.parser
from scrapy.utils.response import open_in_browser
from scrapy.selector import Selector
from ..items import RecruiterboxjobsItem

class CrawlRecruiterBox(scrapy.Spider):
    name = "recruiterBox"
    start_urls = [
        'https://www.google.com/search?&q=site:recruiterbox.com'
    ]

    page_number = 1
    inner_pages = 0
    page_count = 0

    # custom_settings = {
    #     "DOWNLOAD_DELAY": 10,
    #     "CONCURRENT_REQUESTS_PER_DOMAIN": 2
    # }

    # LEVEL-1 CRAWLING

    def parse(self, response):
        html_source = response.body
        html = BeautifulSoup(html_source, 'html.parser')
        with open('../HTML/page' + str(CrawlRecruiterBox.page_number) + '.html', 'w', encoding='utf-8') as f:
            f.write(str(html.prettify()))
        
        next_page = response.xpath('/html/body/div/footer/div[1]/div/div/a/@href').extract_first()

        internal_pages = response.css('a::attr(href)').extract()
        for i in internal_pages:
            url_start = i[0:5]
            if url_start == '/url?':
                inner_url = "https://www.google.com"+i
                yield response.follow(inner_url, callback = self.parseUrl)

        if next_page is not None and CrawlRecruiterBox.page_number < 32:
            CrawlRecruiterBox.page_count += 10
            CrawlRecruiterBox.page_number += 1
            go_next = 'https://www.google.com/search?q=site:recruiterbox.com&start='+str(CrawlRecruiterBox.page_count)
            yield response.follow(go_next, callback = self.parse)

    # LEVEL-2 CRAWLING

    def parseUrl(self, response):
        # open_in_browser(response)
        CrawlRecruiterBox.inner_pages += 1
        html_source = response.body
        html = BeautifulSoup(html_source, 'html.parser')
        with open ('../HTML/Level-2/innerpage'+str(CrawlRecruiterBox.inner_pages)+'.html', 'w', encoding='utf-8') as f:
            f.write(str(html.prettify()))