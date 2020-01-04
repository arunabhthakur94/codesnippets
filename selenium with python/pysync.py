from selenium import webdriver
from bs4 import BeautifulSoup
import html.parser

browser = webdriver.Chrome('/home/arunabh/codebase/Project/chromedriver')
browser.get('https://angel.co/')

html_source = browser.page_source
html = BeautifulSoup(html_source, 'html.parser')
with open('HTML/angellist.html', 'w', encoding='utf-8') as f:
    f.write(str(html.prettify()))

print('Done...')