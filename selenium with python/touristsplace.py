from selenium import webdriver
from bs4 import BeautifulSoup
import html.parser

browser = webdriver.Chrome('/home/arunabh/codebase/Project/chromedriver')
browser.get('https://www.google.com/search?q=tourist+places+in+india&oq=tourist+places+&aqs=chrome.5.69i57j0l7.6502j0j7&sourceid=chrome&ie=UTF-8')

html_source = browser.page_source
html = BeautifulSoup(html_source, 'html.parser')
with open('HTML/touristsplace.html', 'w', encoding ='utf-8') as f:
    f.write(str(html.prettify()))
elems = browser.find_elements_by_xpath("//a[@href]")
for elem in elems:
    print(elem.get_attribute("href"))