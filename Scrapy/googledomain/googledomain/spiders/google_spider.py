import scrapy
from bs4 import BeautifulSoup
import html.parser
from scrapy.utils.response import open_in_browser
from scrapy.selector import Selector
# from selenium import webdriver 
from ..items import GoogledomainItem

class CrawlRecruiterBox(scrapy.Spider):
    name = "scrapRB"
    start_urls = [
        'https://www.google.com/search?&q=site:recruiterbox.com'
    ]

    page_count = 0
    page_number = 1
    inner_pages = 0

    custom_settings = {
        "DOWNLOAD_DELAY": 10,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2
    }

    # LEVEL-2 CRAWLING

    def parseUrl(self, response):
        print("Here RB................................................................................")
        # open_in_browser(response)
        CrawlRecruiterBox.inner_pages += 1
        html_source = response.body
        html = BeautifulSoup(html_source, 'html.parser')
        with open ('../recruiterbox/level1Crawl/innerpage'+str(CrawlRecruiterBox.inner_pages)+'.html', 'w', encoding='utf-8') as f:
            f.write(str(html.prettify()))


    # LEVEL-1 CRAWLNG

    def parse(self, response):
        # open_in_browser(response)
        html_source = response.body
        html = BeautifulSoup(html_source, 'html.parser')
        with open ('../recruiterbox/page'+str(CrawlRecruiterBox.page_number)+'.html', 'w', encoding='utf-8') as f:
            f.write(str(html.prettify()))
        next_page = response.xpath('/html/body/div/footer/div[1]/div/div/a/@href').extract_first()

        internalUrls = response.css('a::attr(href)').extract()
        for i in internalUrls:
            urlStart = i[0:5]
            if urlStart == '/url?':
                inner_url = "https://www.google.com"+i
                yield response.follow(inner_url, callback = self.parseUrl)

        if next_page is not None and CrawlRecruiterBox.page_number < 1:
            CrawlRecruiterBox.page_count += 10
            CrawlRecruiterBox.page_number += 1
            go_next = 'https://www.google.com/search?q=site:recruiterbox.com&start='+str(CrawlRecruiterBox.page_count)
            yield response.follow(go_next, callback = self.parse)
 
            
# class CrawlLeverJobs(scrapy.Spider):
#     name = "leverJobs"
#     allowed_domains = ['lever.co']
#     start_urls = [
#         'https://www.google.com/search?q=site:lever.co'
#     ]

#     page_count = 0
#     file_number = 1
#     inner_pages = 0
    
#     def __init__(self):
#         self.driver = webdriver.Chrome('/home/arunabh/codebase/Project/chromedriver')

    # LEVEL-2 CRAWLING

#     def parseUrl(self, response):
#         print("Here Lever Jobs................................................................................")
#         # open_in_browser(response)
#         CrawlRecruiterBox.inner_pages += 1
#         html_source = self.driver.get(response.body)
#         html = BeautifulSoup(html_source, 'html.parser')
#         with open ('../lever/level1Crawl/innerpage'+str(CrawlRecruiterBox.inner_pages)+'.html', 'w', encoding='utf-8') as f:
#             f.write(str(html.prettify()))
#         self.driver.close()

    # LEVEL-1 CRAWLNG

#     def parse(self, response):
#         # open_in_browser(response)
#         html_source = self.driver.get(response.body)
#         html = BeautifulSoup(html_source, 'html.parser')
#         with open ('../lever/page'+str(CrawlLeverJobs.file_number)+'.html', 'w', encoding='utf-8') as f:
#             f.write(str(html.prettify()))
#         next_page = response.xpath('/html/body/div/footer/div[1]/div/div/a/@href').extract_first()

#         internalUrls = response.css('a::attr(href)').extract()
#         for i in internalUrls:
#             urlStart = i[0:5]
#             if urlStart == '/url?':
#                 inner_url = "https://www.google.com"+i
#                 yield response.follow(inner_url, callback = self.parseUrl)

#         if next_page is not None and CrawlLeverJobs.file_number < 10:
#             CrawlLeverJobs.page_count += 10
#             CrawlLeverJobs.file_number += 1
#             go_next = 'https://www.google.com/search?q=site:lever.co&start='+str(CrawlLeverJobs.page_count)
#             yield response.follow(go_next, callback = self.parse)
        
#         self.driver.close()


class CrawlLeverJobs(scrapy.Spider):
    name = 'scrapLever'
    start_urls = [
        'https://www.google.com/search?q=site:lever.co'
    ]
    page_count = 0
    file_number = 1
    inner_pages = 0

    custom_settings = {
        "DOWNLOAD_DELAY": 10,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2
    }

    # LEVEL-2 CRAWLING

    def parseUrl(self, response):
        print("Here Lever Jobs................................................................................")
        open_in_browser(response)
        CrawlRecruiterBox.inner_pages += 1
        html_source = response.body
        html = BeautifulSoup(html_source, 'html.parser')
        with open ('../lever/level1Crawl/innerpage'+str(CrawlRecruiterBox.inner_pages)+'.html', 'w', encoding='utf-8') as f:
            f.write(str(html.prettify()))

    # LEVEL-1 CRAWLING

    def parse(self, response):
        # open_in_browser(response)
        html_source = response.body
        html = BeautifulSoup(html_source, 'html.parser')
        with open ('../lever/page'+str(CrawlLeverJobs.file_number)+'.html', 'w', encoding='utf-8') as f:
            f.write(str(html.prettify()))
        next_page = response.xpath('/html/body/div/footer/div[1]/div/div/a/@href').extract_first()

        internalUrls = response.css('a::attr(href)').extract()
        for i in internalUrls:
            urlStart = i[0:5]
            if urlStart == '/url?':
                inner_url = "https://www.google.com"+i
                yield response.follow(inner_url, callback = self.parseUrl)

        if next_page is not None and CrawlLeverJobs.file_number < 10:
            CrawlLeverJobs.page_count += 10
            CrawlLeverJobs.file_number += 1
            go_next = 'https://www.google.com/search?q=site:lever.co&start='+str(CrawlLeverJobs.page_count)
            yield response.follow(go_next, callback = self.parse)


class CrawlWorkdayJobs(scrapy.Spider):
    name = 'scrapWorkday'
    start_urls = [
        'https://www.google.com/search?q=site:workday.com'
    ]
    page_count = 0
    file_number = 1
    inner_pages = 0

    custom_settings = {
        "DOWNLOAD_DELAY": 10,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2
    }

    # LEVEL-2 CRAWLING

    def parseUrl(self, response):
        print("Here Lever Jobs................................................................................")
        open_in_browser(response)
        CrawlRecruiterBox.inner_pages += 1
        html_source = response.body
        html = BeautifulSoup(html_source, 'html.parser')
        with open ('../workday/level1Crawl/innerpage'+str(CrawlRecruiterBox.inner_pages)+'.html', 'w', encoding='utf-8') as f:
            f.write(str(html.prettify()))

    # LEVEL-1 CRAWLNG

    def parse(self, response):
        # open_in_browser(response)
        html_source = response.body
        html = BeautifulSoup(html_source, 'html.parser')
        with open ('../workday/page'+str(CrawlWorkdayJobs.file_number)+'.html', 'w', encoding='utf-8') as f:
            f.write(str(html.prettify()))
        next_page = response.xpath('/html/body/div/footer/div[1]/div/div/a/@href').extract_first()
        
        internalUrls = response.css('a::attr(href)').extract()
        for i in internalUrls:
            urlStart = i[0:5]
            if urlStart == '/url?':
                inner_url = "https://www.google.com"+i
                yield response.follow(inner_url, callback = self.parseUrl)


        if next_page is not None and CrawlWorkdayJobs.file_number < 10:
            CrawlWorkdayJobs.page_count += 10
            CrawlWorkdayJobs.file_number += 1
            go_next = 'https://www.google.com/search?q=site:workday.com&start='+str(CrawlWorkdayJobs.page_count)
            yield response.follow(go_next, callback = self.parse)


class CrawlLinkUp(scrapy.Spider):
    name = 'scrapLinkUp'
    start_urls = [
        'https://www.google.com/search?q=site:linkup.com'
    ]
    page_count = 0
    file_number = 1
    inner_pages = 0

    custom_settings = {
        "DOWNLOAD_DELAY": 10,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2
    }

    # LEVEL-2 CRAWLING

    def parseUrl(self, response):
        print("Here Linkup Jobs................................................................................")
        open_in_browser(response)
        CrawlRecruiterBox.inner_pages += 1
        html_source = response.body
        html = BeautifulSoup(html_source, 'html.parser')
        with open ('../linkUp/level1Crawl/innerpage'+str(CrawlRecruiterBox.inner_pages)+'.html', 'w', encoding='utf-8') as f:
            f.write(str(html.prettify()))

    # LEVEL-1 CRAWLNG

    def parse(self, response):
        # open_in_browser(response)
        html_source = response.body
        html = BeautifulSoup(html_source, 'html.parser')
        with open ('../linkUp/page'+str(CrawlLinkUp.file_number)+'.html', 'w', encoding='utf-8') as f:
            f.write(str(html.prettify()))
        next_page = response.xpath('/html/body/div/footer/div[1]/div/div/a/@href').extract_first()

        internalUrls = response.css('a::attr(href)').extract()
        for i in internalUrls:
            urlStart = i[0:5]
            if urlStart == '/url?':
                inner_url = "https://www.google.com"+i
                yield response.follow(inner_url, callback = self.parseUrl)

        if next_page is not None and CrawlLinkUp.file_number < 10:
            CrawlLinkUp.page_count += 10
            CrawlLinkUp.file_number += 1
            go_next = 'https://www.google.com/search?q=site:linkup.com&start='+str(CrawlLinkUp.page_count)
            yield response.follow(go_next, callback = self.parse)


class CrawlZipRecruiter(scrapy.Spider):
    name = 'scrapZipRecruiter'
    start_urls = [
        'https://www.google.com/search?q=site:ziprecruiter.com'
    ]
    page_count = 0
    file_number = 1
    inner_pages = 0

    custom_settings = {
        "DOWNLOAD_DELAY": 10,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2
    }

    # LEVEL-2 CRAWLING

    def parseUrl(self, response):
        print("Here Zip Recruiter Jobs................................................................................")
        open_in_browser(response)
        CrawlRecruiterBox.inner_pages += 1
        html_source = response.body
        html = BeautifulSoup(html_source, 'html.parser')
        with open ('../ziprecruiter/level1Crawl/innerpage'+str(CrawlRecruiterBox.inner_pages)+'.html', 'w', encoding='utf-8') as f:
            f.write(str(html.prettify()))

    # LEVEL-1 CRAWLNG

    def parse(self, response):
        # open_in_browser(response)
        html_source = response.body
        html = BeautifulSoup(html_source, 'html.parser')
        with open ('../ziprecruiter/page'+str(CrawlZipRecruiter.file_number)+'.html', 'w', encoding='utf-8') as f:
            f.write(str(html.prettify()))
        next_page = response.xpath('/html/body/div/footer/div[1]/div/div/a/@href').extract_first()

        internalUrls = response.css('a::attr(href)').extract()
        # print(internalUrls)
        for i in internalUrls:
            urlStart = i[0:5]
            if urlStart == '/url?':
                inner_url = "https://www.google.com"+i
                yield response.follow(inner_url, callback = self.parseUrl)

        if next_page is not None and CrawlZipRecruiter.file_number < 10:
            CrawlZipRecruiter.page_count += 10
            CrawlZipRecruiter.file_number += 1
            go_next = 'https://www.google.com/search?q=site:ziprecruiter.com&start='+str(CrawlZipRecruiter.page_count)
            yield response.follow(go_next, callback = self.parse)


class CrawlSimplyHired(scrapy.Spider):
    name = 'scrapSimplyHired'
    start_urls = [
        'https://www.google.com/search?q=site:simplyHired.com'
    ]
    page_count = 0
    file_number = 1
    inner_pages = 0

    custom_settings = {
        "DOWNLOAD_DELAY": 10,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2
    }

    # LEVEL-2 CRAWLING

    def parseUrl(self, response):
        print("Here Simply Hired Jobs................................................................................")
        open_in_browser(response)
        CrawlRecruiterBox.inner_pages += 1
        html_source = response.body
        html = BeautifulSoup(html_source, 'html.parser')
        with open ('../simplyHired/level1Crawl/innerpage'+str(CrawlRecruiterBox.inner_pages)+'.html', 'w', encoding='utf-8') as f:
            f.write(str(html.prettify()))

    # LEVEL-1 CRAWLNG

    def parse(self, response):
        # open_in_browser(response)
        html_source = response.body
        html = BeautifulSoup(html_source, 'html.parser')
        with open ('../simplyHired/page'+str(CrawlSimplyHired.file_number)+'.html', 'w', encoding='utf-8') as f:
            f.write(str(html.prettify()))
        next_page = response.xpath('/html/body/div/footer/div[1]/div/div/a/@href').extract_first()

        internalUrls = response.css('a::attr(href)').extract()
        for i in internalUrls:
            urlStart = i[0:5]
            if urlStart == '/url?':
                inner_url = "https://www.google.com"+i
                yield response.follow(inner_url, callback = self.parseUrl)

        if next_page is not None and CrawlSimplyHired.file_number < 10:
            CrawlSimplyHired.page_count += 10
            CrawlSimplyHired.file_number += 1
            go_next = 'https://www.google.com/search?q=site:simplyHired.com&start='+str(CrawlSimplyHired.page_count)
            yield response.follow(go_next, callback = self.parse)


class CrawlCareerBuilder(scrapy.Spider):
    name = 'scrapCareerBuilder'
    start_urls = [
        'https://www.google.com/search?q=site:careerbuilder.com'
    ]
    page_count = 0
    file_number = 1
    inner_pages = 0

    custom_settings = {
        "DOWNLOAD_DELAY": 10,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2
    }

    # LEVEL-2 CRAWLING

    def parseUrl(self, response):
        print("Here Career Builder Jobs................................................................................")
        # open_in_browser(response)
        CrawlRecruiterBox.inner_pages += 1
        html_source = response.body
        html = BeautifulSoup(html_source, 'html.parser')
        with open ('../careerBuilder/level1Crawl/innerpage'+str(CrawlRecruiterBox.inner_pages)+'.html', 'w', encoding='utf-8') as f:
            f.write(str(html.prettify()))

    # LEVEL-1 CRAWLNG

    def parse(self, response):
        # open_in_browser(response)
        html_source = response.body
        html = BeautifulSoup(html_source, 'html.parser')
        with open ('../careerBuilder/page'+str(CrawlCareerBuilder.file_number)+'.html', 'w', encoding='utf-8') as f:
            f.write(str(html.prettify()))
        next_page = response.xpath('/html/body/div/footer/div[1]/div/div/a/@href').extract_first()

        internalUrls = response.css('a::attr(href)').extract()
        for i in internalUrls:
            urlStart = i[0:5]
            if urlStart == '/url?':
                inner_url = "https://www.google.com"+i
                yield response.follow(inner_url, callback = self.parseUrl)

        if next_page is not None and CrawlCareerBuilder.file_number < 10:
            CrawlCareerBuilder.page_count += 10
            CrawlCareerBuilder.file_number += 1
            go_next = 'https://www.google.com/search?q=site:careerbuilder.com&start='+str(CrawlCareerBuilder.page_count)
            yield response.follow(go_next, callback = self.parse)


class CrawlSnagaJobs(scrapy.Spider):
    name = 'scrapSnagaJobs'
    start_urls = [
        'https://www.google.com/search?q=site:snagajob.com'
    ]
    page_count = 0
    file_number = 1
    inner_pages = 0

    custom_settings = {
        "DOWNLOAD_DELAY": 10,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2
    }

    # LEVEL-2 CRAWLING

    def parseUrl(self, response):
        print("Here Snaga Jobs Jobs................................................................................")
        open_in_browser(response)
        CrawlRecruiterBox.inner_pages += 1
        html_source = response.body
        html = BeautifulSoup(html_source, 'html.parser')
        with open ('../snagaJob/level1Crawl/innerpage'+str(CrawlRecruiterBox.inner_pages)+'.html', 'w', encoding='utf-8') as f:
            f.write(str(html.prettify()))

    # LEVEL-1 CRAWLNG

    def parse(self, response):
        # open_in_browser(response)
        html_source = response.body
        html = BeautifulSoup(html_source, 'html.parser')
        with open ('../snagaJob/page'+str(CrawlSnagaJobs.file_number)+'.html', 'w', encoding='utf-8') as f:
            f.write(str(html.prettify()))
        next_page = response.xpath('/html/body/div/footer/div[1]/div/div/a/@href').extract_first()

        internalUrls = response.css('a::attr(href)').extract()
        for i in internalUrls:
            urlStart = i[0:5]
            if urlStart == '/url?':
                inner_url = "https://www.google.com"+i
                yield response.follow(inner_url, callback = self.parseUrl)

        if next_page is not None and CrawlSnagaJobs.file_number < 10:
            CrawlSnagaJobs.page_count += 10
            CrawlSnagaJobs.file_number += 1
            go_next = 'https://www.google.com/search?q=site:snagajob.com&start='+str(CrawlSnagaJobs.page_count)
            yield response.follow(go_next, callback = self.parse)


class CrawlJobs(scrapy.Spider):
    name = 'scrapJobs'
    start_urls = [
        'https://www.google.com/search?q=site:job.com'
    ]
    page_count = 0
    file_number = 1
    inner_pages = 0

    custom_settings = {
        "DOWNLOAD_DELAY": 10,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2
    }

    # LEVEL-2 CRAWLING

    def parseUrl(self, response):
        print("Here Jobs Jobs................................................................................")
        open_in_browser(response)
        CrawlRecruiterBox.inner_pages += 1
        html_source = response.body
        html = BeautifulSoup(html_source, 'html.parser')
        with open ('../job/level1Crawl/innerpage'+str(CrawlRecruiterBox.inner_pages)+'.html', 'w', encoding='utf-8') as f:
            f.write(str(html.prettify()))

    # LEVEL-1 CRAWLNG

    def parse(self, response):
        # open_in_browser(response)
        html_source = response.body
        html = BeautifulSoup(html_source, 'html.parser')
        with open ('../job/page'+str(CrawlJobs.file_number)+'.html', 'w', encoding='utf-8') as f:
            f.write(str(html.prettify()))
        next_page = response.xpath('/html/body/div/footer/div[1]/div/div/a/@href').extract_first()

        internalUrls = response.css('a::attr(href)').extract()
        for i in internalUrls:
            urlStart = i[0:5]
            if urlStart == '/url?':
                inner_url = "https://www.google.com"+i
                yield response.follow(inner_url, callback = self.parseUrl)

        if next_page is not None and CrawlJobs.file_number < 10:
            CrawlJobs.page_count += 10
            CrawlJobs.file_number += 1
            go_next = 'https://www.google.com/search?q=site:job.com&start='+str(CrawlJobs.page_count)
            yield response.follow(go_next, callback = self.parse)



class crawlPost(scrapy.Spider):
    name = "rbjob"
    start_urls = [
        # 'https://mainebhr.recruiterbox.com/jobs/fk034h5/',
        # 'https://mainebhr.recruiterbox.com/jobs/fk03zw4/',
        'file:///home/arunabh/codebase/Project/Scrapy/googledomain/googledomain/recruiterbox/level1Crawl/innerpage1.html'

    ]
    next_job = 1

    def parse(self, response):
        jobs = response.css('a::attr(href)').extract()
        for i in jobs:
            if i[0:6] == '/jobs/':
                url = "https://mainebhr.recruiterbox.com"+i
                yield response.follow(url, callback = self.parseJob)

        crawlPost.next_job += 1
        go_next = 'file:///home/arunabh/codebase/Project/Scrapy/googledomain/googledomain/recruiterbox/level1Crawl/innerpage'+str(crawlPost.next_job)+'.html'
        yield response.follow(go_next, callback = self.parse)


    
    def parseJob(self, response):
        items = GoogledomainItem()

        # open_in_browser(response)
        job_title = response.css('#content > div > div > header > h1::text').extract_first()
        location = response.css('#content > div > div > header > p > span::text').extract_first()
        job_type = response.css('#content > div > div > header > p > small:nth-child(2)::text').extract_first()
        description = response.css('#content > div > div > div > div.col-md-9 > div > p:nth-child(5) > span::text').extract_first()

        items['job_title'] = job_title
        items['location'] = location
        if job_type is not None:
            items['job_type'] = job_type
        else:
            items['job_type'] = 'Full-time'
        if description is not None:
            items['description'] = description
        else:
            items['description'] = 'Our'+job_title+' will be the master of all things content execution and strategy. Your objective will be to generate content that is aligned with our positioning, thought leadership, Inbound and demand generation strategy. You will need to conduct user persona research, competitive research, keyword research, topic research, create a list of content topics and organize them in a content calendar, write some compelling content yourself, assign the right content topic(s) to the right freelancer/ agency, supervise and approve their work, make sure content is properly linked internally and externally, launch the content on our website / blog/ email list/ newsletter, track traffic and conversion overtime and assist with tweaking content to improve conversion. Own the impact content has on site traffic, demo request/ trial conversion and wins. The role will report to the VP-Product Marketing who reports to the CEO.'
        yield items































































































































































    # LEVEL-1 CRAWLNG

    # def parse(self, response):
    #     open_in_browser(response)
    #     page = response.url.split("/")[-1]
    #     filename = 'quotes-%s.html' % page
    #     with open ('../recruiterbox/page'+str(CrawlMultiplePages.page_number)+'.html', 'wb') as f:
    #         f.write(response.body)
    #         self.log('Saved file %s' % filename)
    #     next_page = Selector(response=response).xpath('/html/body/div/footer/div[1]/div/div/a/@href').get()
    #     if next_page is not None:
    #         CrawlMultiplePages.page_number += 1 
    #         next_page = response.urljoin(next_page)
    #         yield scrapy.Request(next_page, callback=self.parse)
    # next_page = response.urljoin(next_page)
            # yield response.follow(next_page, callback = self.parse)

            # next_page
            # CrawlMultiplePages.page_count += 10
            # CrawlMultiplePages.page_number += 1
            # go_next = 'https://www.google.com/search?q=site:recruiterbox.com&sxsrf=ACYBGNQdfK4mvEdYBZzjq6WmwMgxwaxp0w:1577513615729&ei=j_IGXsOYLNKW4-EPiZOXgAk&start='+str(CrawlMultiplePages.page_count)+'&sa=N&ved=2ahUKEwiDnMaV2NfmAhVSyzgGHYnJBZAQ8tMDegQICxAu&biw=1366&bih=696'
            # yield response.follow(next_page, callback = self.parse)

        # if CrawlMultiplePages.page_count == 0:
        #     next_page = response.xpath('/html/body/div/footer/div[1]/div/div/a/text()').extract_first()
        #     print("Here")
        #     CrawlMultiplePages.page_count += 10
        #     CrawlMultiplePages.page_number += 1
        #     go_next = 'https://www.google.com/search?q=site:recruiterbox.com&sxsrf=ACYBGNQdfK4mvEdYBZzjq6WmwMgxwaxp0w:1577513615729&ei=j_IGXsOYLNKW4-EPiZOXgAk&start='+str(CrawlMultiplePages.page_count)+'&sa=N&ved=2ahUKEwiDnMaV2NfmAhVSyzgGHYnJBZAQ8tMDegQICxAu&biw=1366&bih=696'
        #     yield response.follow(go_next, callback = self.parse)

        # elif CrawlMultiplePages.page_count == 10:
        #     next_page = response.xpath('/html/body/div/footer/div[1]/div/div/a[2]/span/text()').extract_first()
        #     print(next_page)
        #     if next_page == '>':
        #         print("At second page")
        #         CrawlMultiplePages.page_count += 10
        #         CrawlMultiplePages.page_number += 1
        #         go_next = 'https://www.google.com/search?q=site:recruiterbox.com&sxsrf=ACYBGNQdfK4mvEdYBZzjq6WmwMgxwaxp0w:1577513615729&ei=j_IGXsOYLNKW4-EPiZOXgAk&start='+str(CrawlMultiplePages.page_count)+'&sa=N&ved=2ahUKEwiDnMaV2NfmAhVSyzgGHYnJBZAQ8tMDegQICxAu&biw=1366&bih=696'
        #         yield response.follow(go_next, callback = self.parse)
        # else:
        #     next_page = response.xpath('/html/body/div/footer/div[1]/div/div/a[3]/span/text()').extract_first()
        #     if next_page == '>' and CrawlMultiplePages.page_count > 10:
        #         print("Now Here")
        #         CrawlMultiplePages.page_count += 10
        #         CrawlMultiplePages.page_number += 1
        #         go_next = 'https://www.google.com/search?q=site:recruiterbox.com&sxsrf=ACYBGNQdfK4mvEdYBZzjq6WmwMgxwaxp0w:1577513615729&ei=j_IGXsOYLNKW4-EPiZOXgAk&start='+str(CrawlMultiplePages.page_count)+'&sa=N&ved=2ahUKEwiDnMaV2NfmAhVSyzgGHYnJBZAQ8tMDegQICxAu&biw=1366&bih=696'
        #         yield response.follow(go_next, callback = self.parse)


        




    # def parse(self, response):
    #     global page_number
    #     global counter
    #     page_number = 1
    #     # open_in_browser(response)
    #     html_source = response.body
    #     html = BeautifulSoup(html_source, 'html.parser')
    #     with open ('../recruiterbox/page'+str(page_number)+'.html', 'w', encoding='utf-8') as f:
    #         f.write(str(html.prettify()))
    #         span = response.xpath('/html/body/div/footer/div[1]/div/div/a').extract()
            # print(span)
            # next_flag = False
            # if(len(span) != 0):
            #     next_flag = True
            #     counter = 10
            #     page_number = 2
            #     while next_flag:
            #         next_page_url = 'https://www.google.com/search?q=site:recruiterbox.com&sxsrf=ACYBGNSJgyV9Oe-IsEjIlRr0RxUwl1VjAA:1577494051108&ei=I6YGXqSkBoGGmgeIvIPICw&start='+str(counter)+'&sa=N&ved=2ahUKEwjkwbSkj9fmAhUBg-YKHQjeALkQ8tMDegQICxAu&biw=675&bih=683'
            #         if next_page_url is not None:
            #             page_number += 1
            #             yield response.follow(next_page_url, callback = self.parse)

        
        # Our Senior Manager / Director, Content Marketing will be the master of all things content execution and strategy. Your objective will be to generate content that is aligned with our positioning, thought leadership, Inbound and demand generation strategy. You will need to conduct user persona research, competitive research, keyword research, topic research, create a list of content topics and organize them in a content calendar, write some compelling content yourself, assign the right content topic(s) to the right freelancer/ agency, supervise and approve their work, make sure content is properly linked internally and externally, launch the content on our website / blog/ email list/ newsletter, track traffic and conversion overtime and assist with tweaking content to improve conversion. Own the impact content has on site traffic, demo request/ trial conversion and wins. The role will report to the VP-Product Marketing who reports to the CEO.