import scrapy
from bs4 import BeautifulSoup
import html.parser
from scrapy.utils.response import open_in_browser
from scrapy.selector import Selector
from ..items import RecruiterboxjobsItem
import csv

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
        with open('/tmp/HTML/page' + str(CrawlRecruiterBox.page_number) + '.html', 'w', encoding='utf-8') as f:
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


# Parsing Jobs

class crawlPost(scrapy.Spider):
    name = "rbjob"
    start_urls = [
        'file:///home/arunabh/codebase/Project/Scrapy/recruiterboxjobs/recruiterboxjobs/html_rb/innerpage1.html'

    ]
    next_job = 1

    def parse(self, response):
        jobs = response.css('a::attr(href)').extract()
        for i in jobs:
            if i[0:6] == '/jobs/':
                url = "https://mainebhr.recruiterbox.com"+i
                yield response.follow(url, callback = self.parseJob)

        crawlPost.next_job += 1
        go_next = 'file:///home/arunabh/codebase/Project/Scrapy/recruiterboxjobs/recruiterboxjobs/html_rb/innerpage'+str(crawlPost.next_job)+'.html'
        yield response.follow(go_next, callback = self.parse)


    
    def parseJob(self, response):
        # open_in_browser(response)
        count = 1
        job_title = response.xpath('/html/body/div[2]/div/div/header/h1/text()').extract()
        company_name = response.xpath('/html/body/div[1]/div/div/div/div[1]/a/img/@alt').extract()
        description = response.xpath('/html/body/div[2]/div/div/div/div[1]/div/p[26]/text()').extract()
        payscale = 'Best In Industry'
        location = response.xpath('/html/body/div[2]/div/div/header/p/span/text()').extract()
        job_type = response.xpath('/html/body/div[2]/div/div/header/p/small/text()').extract()
        company_type = None
        date_posted = 'Yesterday'
        parent_source = response.xpath('/html/body/div[2]/div/div/div/div[1]/section/div[1]/div[1]/div[1]/a/@href').extract()
        active = 'True'
        if len(job_type) == 0:
            job_type = 'Full-time'
        if len(description) == 0:
            description = 'Our'+job_title+' will be the master of all things content execution and strategy. Your objective will be to generate content that is aligned with our positioning, thought leadership, Inbound and demand generation strategy. You will need to conduct user persona research, competitive research, keyword research, topic research, create a list of content topics and organize them in a content calendar, write some compelling content yourself, assign the right content topic(s) to the right freelancer/ agency, supervise and approve their work, make sure content is properly linked internally and externally, launch the content on our website / blog/ email list/ newsletter, track traffic and conversion overtime and assist with tweaking content to improve conversion. Own the impact content has on site traffic, demo request/ trial conversion and wins. The role will report to the VP-Product Marketing who reports to the CEO.'

        with open ('../jobs.csv','a') as csvfile:
            fieldnames = ['job_title', 'company_name', 'description', 'payscale', 'location', 'job_type', 'company_type', 'date_posted', 'parent_source', 'active']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if count == 1:
                writer.writeheader()
                count += 1
            writer.writerow({
                'job_title': job_title,
                'company_name': company_name,
                'description': description,
                'payscale': payscale,
                'location': location,
                'job_type': job_type,
                'company_type': company_type,
                'date_posted': date_posted,
                'parent_source': parent_source,
                'active': active
            })
        yield None
