import scrapy
from bs4 import BeautifulSoup
import csv

class CrawlLeverJobs(scrapy.Spider):
    name = 'scrapLever'
    start_urls = [
        'https://www.google.com/search?q=site:lever.co'
    ]
    page_count = 0
    file_number = 1
    inner_pages = 0

    # LEVEL-1 CRAWLING

    def parse(self, response):
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

        if next_page is not None and CrawlLeverJobs.file_number < 30:
            CrawlLeverJobs.page_count += 10
            CrawlLeverJobs.file_number += 1
            go_next = 'https://www.google.com/search?q=site:lever.co&start='+str(CrawlLeverJobs.page_count)
            yield response.follow(go_next, callback = self.parse)

        
    # LEVEL-2 CRAWLING

    def parseUrl(self, response):
        # open_in_browser(response)
        CrawlLeverJobs.inner_pages += 1
        html_source = response.body
        html = BeautifulSoup(html_source, 'html.parser')
        with open ('../lever/level1Crawl/innerpage'+str(CrawlLeverJobs.inner_pages)+'.html', 'w', encoding='utf-8') as f:
            f.write(str(html.prettify()))



class crawlLever(scrapy.Spider):
    name = 'leverscraper'
    start_urls = ['file////home/masai/Documents/lever/innerpage1.html']

    next_job = 1

    def parse(self, response):
        jobs = response.xpath('//a[contains(@href, "jobs")]/@href').getall()
        for i in jobs:
            yield response.follow(i, callback=self.parseJob)
    
    def parseJob(self, response):
        # open_in_browser(response)
        count = 1
        job_title = response.xpath('//h2/text()').extract_first()
        company_name = response.xpath('').extract()
        description = response.xpath('//div[(((count(preceding-sibling::*) + 1) = 7) and parent::*)]/text()').extract()
        payscale = 'Best In Industry'
        location=response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "sort-by-time", " " ))]/text()').extract_first()
        job_type = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "sort-by-commitment", " " ))]/text()').extract_first()
        company_type = None
        date_posted = 'Yesterday'
        parent_source = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "black", " " ))]/@href').extract_first()
        active = 'True'
        if len(job_type) == 0:
            job_type = 'Full-time'
        if len(description) == 0:
            description = 'Our'+job_title+' will be the master of all things content execution and strategy. Your objective will be to generate content that is aligned with our positioning, thought leadership, Inbound and demand generation strategy. You will need to conduct user persona research, competitive research, keyword research, topic research, create a list of content topics and organize them in a content calendar, write some compelling content yourself, assign the right content topic(s) to the right freelancer/ agency, supervise and approve their work, make sure content is properly linked internally and externally, launch the content on our website / blog/ email list/ newsletter, track traffic and conversion overtime and assist with tweaking content to improve conversion. Own the impact content has on site traffic, demo request/ trial conversion and wins. The role will report to the VP-Product Marketing who reports to the CEO.'

        with open ('../leverjobs.csv','a') as csvfile:
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
