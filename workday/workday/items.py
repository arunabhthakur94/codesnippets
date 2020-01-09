# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WorkdayItem(scrapy.Item):
    job_title = scrapy.Field()
    location  = scrapy.Field()
    job_type = scrapy.Field()
    description = scrapy.Field()
    parent_source = scrapy.Field()
    date_posted = scrapy.Field()
    company_type = scrapy.Field()
    pay_scale = scrapy.Field()
    company_name = scrapy.Field()
