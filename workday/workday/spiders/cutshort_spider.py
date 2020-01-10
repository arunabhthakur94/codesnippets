import scrapy
from bs4 import BeautifulSoup
import bs4
# from HTMLParser import HTMLParser
# import HTMLParser
import csv
import json
from scrapy.utils.response import open_in_browser
from scrapy.selector import Selector
from ..items import WorkdayItem
 
class CrawlworkDay(scrapy.Spider):
    name = "cutshort"
    start_urls = [
        'https://cutshort.io/sitemap'
    ]
 
    page_count = 0
    page_number = 1
    inner_pages = 0
    
    # custom_settings = {
    #     "DOWNLOAD_DELAY" : 10,
    #     "CONCURRENT_REQUESTS_PER_DOMAIN": 2
    # }
  
    # Level - 1 Crawling

    def parse(self,response):
        html_source = response.css('a::attr(href)').extract()
        html = BeautifulSoup(str(html_source), 'html.parser')
        arr = []
        arr.append(html)
        with open ('../cutshortfetched/level1data/datas.csv','w', encoding='utf-8') as csvfile:
            fieldnames = ['url']
            writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
            # writer.writeheader()
            for i in range(len(arr)):
                writer.writerow({'url': str(html.prettify())})
         
        innerUrls = response.css('a::attr(href)').extract()
        for i in innerUrls:
            url = i[0:6]
            if url == '/jobs/':
                inner_url = "https://cutshort.io/"+i
                yield response.follow(inner_url, callback = self.parselvl2)

    # Level - 2 Crawling

    def parselvl2(self,response):
        job_title=response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "text_ellipsis", " " )) and contains(concat( " ", @class, " " ), concat( " ", "inline_top", " " ))]/text()').extract_first()
        company_name = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "text_ellipsis", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "everyOtherLink", " " ))]/text()').extract_first()
        pay_scale  = payscale= response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "mr20", " " ))]//span/text()').extract_first()
        location = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "mr20", " " )) and (((count(preceding-sibling::*) + 1) = 1) and parent::*)]//*[contains(concat( " ", @class, " " ), concat( " ", "inline_middle", " " ))]/text()').extract_first()
        parent_source = "https://cutshort.io/jobs/growth-hacking-jobs-in-bangalore-bengaluru"
        job_type = "Full time"
        company_type = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "t", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "t", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "inline_middle", " " )) and (((count(preceding-sibling::*) + 1) = 3) and parent::*)]//span/text()').extract_first()
        apply_now = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "everyOtherBlueButton", " " ))]/@href').extract_first()
        arr_company_name = []
        arr_company_name.append(company_name)

        arr_job_title = []
        arr_job_title.append(arr_job_title)

        arr_pay_scale = []
        arr_pay_scale.append(pay_scale)
        
        arr_location = []
        arr_location.append(location)

        arr_parent_source = []
        arr_parent_source.append(parent_source)

        arr_job_type = []
        arr_job_type.append(job_type)

        arr_company_name = []
        arr_company_name.append(company_name)

        arr_apply_now = []
        arr_apply_now.append(apply_now)

        with open ('../cutshortfetched/level2data/datas.csv','a', encoding='utf-8') as csvfile:
            fieldnames = ['Job_Title','Company_Name','Pay_Scale','Location','Parent_Source','Job_Type','Company_Type','Apply_Now']
            writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
            # writer.writeheader()
            for i in range(len(arr_company_name)):
                writer.writerow({'Job_Title': [job_title],'Company_Name': company_name, 'Pay_Scale': pay_scale, 'Location':location,'Parent_Source':parent_source,'Job_Type':job_type, 'Company_Type':company_type, 'Apply_Now':apply_now})
            return json.dumps({"response": "done"})
        yield None



    
