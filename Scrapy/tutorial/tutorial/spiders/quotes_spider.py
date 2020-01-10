import scrapy
from ..items import TutorialItem
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser

# Scraping only one element from the web

class IntegrateGCS(scrapy.Spider):
    name = "gcs"
    start_urls = [
        'http://quotes.toscrape.com/'
    ]

    def parse(self, response):
        open_in_browser(response)
        yield response.body

class QuoteSpider(scrapy.Spider):
    name = "quotes1"
    start_urls = [
        'http://quotes.toscrape.com/'
    ]

    def parse(self, response):
        title = response.css('title::text').extract()
        yield {
            'title-text': title
        }


# V9: Extracting data with CSS Selector
# Using Shell inside the Scrapy
# open shell : scrapy shell [URl]

# 1. select a tag
# response.css('title').extract()
# 2. select content of the tag
# response.css('title::text').extract()
# 3. Get text only
# response.css('title::text').extract_first()
# response.css('title::text')[0].extract()
# 4. Get all quotes
# response.css('span.text::text').extract()
# 5. Get any particular quote
# response.css('span.text::text')[3].extract()


# V10: Extracting data with XPATH
# Using Shell inside the Scrapy
# open shell : scrapy shell [URL]

# 1. select a tag
# response.xpath('//title').extract()
# 2. select content of the tag
# response.xpath('//title/text()').extract()
# 4. Get all quotes
# response.xpath("//span[@class='text]/text()").extract()
# 5. Get any particular quote
# response.xpath("//span[@class='text]/text()")[1].extract()

# Combination of CSS Selector and xpath
# response.css("li.next a").xpath("@href").extract()


# V11. Web Scraping Quotes and Authors

class QuoteAuthorSpider(scrapy.Spider):
    name = "quotesAuthors"
    start_urls = [
        'http://quotes.toscrape.com/'
    ]

    def parse(self, response):
        all_div_quotes = response.css('div.quote')
        print(all_div_quotes)

        # for quote in all_div_quotes:
        #     title = quote.css('span.text::text').extract()
        #     author = quote.css('.author::text').extract()
        #     tags = quote.css('.tag::text').extract()

        #     yield {
        #         'title': title,
        #         'author': author,
        #         'tags': tags
        #     }


# V12. Items Container(Storing scraped data)
# use of items.py file
# Used as temp locations to store data

# class QuoteAuthorSpider(scrapy.Spider):
#     name = "storingItems"
#     start_urls = [
#         'http://quotes.toscrape.com/'
#     ]

#     def parse(self, response):
#         items = TutorialItem()

#         all_div_quotes = response.css('div.quote')

#         for quote in all_div_quotes:
#             items['title'] = quote.css('span.text::text').extract()
#             items['author'] = quote.css('.author::text').extract()
#             items['tag'] = quote.css('.tag::text').extract()

#             yield items


# V13. Storing data XML,CSV,JSON or HTML
# scrapy crawl storingItems -o items.json

# V14. Pipelines used to connect DB
# Scraped data -> Item Container -> pipeline -> DB

# V15 and V16. Sending data to the DB (MySQL)
# database.py AND pipeline.py

# V17. Sending data to MySQL Lite DB
# V18. Sending data to Mongo DB

# V19. Crawling mulitple pages

class CrawlMultiplePages(scrapy.Spider):
    name = "multiplePages"
    start_urls = [
        'http://quotes.toscrape.com/'
    ]

    def parse(self, response):
        items = TutorialItem()

        all_div_quotes = response.css('div.quote')

        for quote in all_div_quotes:
            title = quote.css('span.text::text').extract()
            author = quote.css('.author::text').extract()
            tag = quote.css('.tag::text').extract()

            items['title'] = title
            items['author'] = author
            items['tag'] = tag

            yield items
        
        next_page = response.css('li.next a::attr(href)').get()

        if next_page is not None:
            yield response.follow(next_page, callback = self.parse)


# V20. Crawling with pagination 

class CrawlPagination(scrapy.Spider):
    name = "pagination"
    page_number = 2
    start_urls = [
        "http://quotes.toscrape.com/page/1/"
    ]

    def parse(self, response):
        items = TutorialItem()

        all_div_quotes = response.css('div.quote')

        for quote in all_div_quotes:
            title = quote.css('span.text::text').extract()
            author = quote.css('.author::text').extract()
            tag = quote.css('.tag::text').extract()

            items['title'] = title
            items['author'] = author
            items['tag'] = tag

            yield items
        
        next_page = 'http://quotes.toscrape.com/page/'+str(CrawlPagination.page_number)+'/'

        if CrawlPagination.page_number < 11:
            CrawlPagination.page_number += 1
            yield response.follow(next_page, callback = self.parse)


# V21. LOGIN functionality

# class LoginSpider(scrapy.Spider):
#     name = "login"
#     start_urls = [
#         'http://quotes.toscrape.com/login'
#     ]

#     def parse(self, response):
#         token = response.css('form input::attr(value)').extract_first()
#         return FormRequest.from_response(response, formdata={
#             "csrf_token": token,
#             "username": 'arunabhsingh',
#             'password': '12345'
#         }, callback = self.start_scraping)


#     def start_scraping(self, response):
#         open_in_browser(response)
#         items = TutorialItem()

#         all_div_quotes = response.css('div.quote')

#         for quote in all_div_quotes:
#             items['title'] = quote.css('span.text::text').extract()
#             items['author'] = quote.css('.author::text').extract()
#             items['tag'] = quote.css('.tag::text').extract()

#             yield items


# V22. Scraping Amazon

class AmazonScrapy(scrapy.Spider):
    name = "amazon"
    start_urls = [
        'https://www.amazon.in/s?i=stripbooks&bbn=4149418031&rh=n%3A976389031%2Cn%3A976390031%2Cn%3A15417300031%2Cn%3A4149418031%2Cp_n_publication_date%3A2684819031&dc&page=2&fst=as%3Aoff&qid=1577432275&rnid=2684818031&ref=sr_pg_2'
    ]

    def parse(self, response):
        with open('amazon.html', 'wb') as f:
            f.write(response.body)

        items = TutorialItem()

        title = response.css('.a-color-base.a-text-normal').css('::text').extract()
        price = response.css('.a-spacing-top-small .a-price-whole').css('::text').extract()
        image = response.css('.s-image::attr(src)').extract()
        author = response.css('.a-color-secondary .a-size-base:nth-child(2)').css('::text').extract()

        items['title'] = title
        items['price'] = price
        items['author'] = author
        items['image'] = image

        yield items


# V23. User-Agents to bypass website restrictions 

# V24. Bypass using Proxies