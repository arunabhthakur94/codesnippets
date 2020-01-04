import sys
from selenium import webdriver
from bs4 import BeautifulSoup
import html.parser

search_input = sys.argv[1]
parent_url = 'https://www.google.com/search?q='+search_input

browser = webdriver.Chrome('/home/arunabh/codebase/Project/chromedriver')
browser.get(parent_url)

html_source = browser.page_source
html = BeautifulSoup(html_source, 'html.parser')
with open('practice/'+search_input+'.html', 'w', encoding='utf-8') as f:
    f.write(str(html.prettify()))
    span = html.body.findAll(text='Next')
    print(span)
    if(len(span) != 0):
        next_flag = True
        counter = 10
        page_number = 2
        while next_flag:
            next_pages_url = 'https://www.google.com/search?q=india&sxsrf=ACYBGNRygruln0u1Sh9QdmtDg8r87uAHeQ:1576814445042&ei=bUf8XeGoAtqb9QOpuK2oBQ&start='+str(counter)+'&sa=N&ved=2ahUKEwihk_7Gq8PmAhXaTX0KHSlcC1UQ8tMDegQIEhAw&biw=1366&bih=696'
            print(next_pages_url)
            browser.get(next_pages_url)

            html_source = browser.page_source
            html = BeautifulSoup(html_source, 'html.parser')
            with open('practice/'+search_input+str(page_number)+'.html', 'w', encoding='utf-8') as f:
                f.write(str(html.prettify()))
                span = html.body.findAll(text='Next')
                if(len(span) != 0):
                    counter += 10
                    page_number += 1
                else:
                    next_flag = False
    else:
        print(False)