# pip3 install requests beautifulsoup4
import requests
from bs4 import BeautifulSoup
import re
import csv

target_url = ""
urls_to_visit = [target_url]

# set a maximum crawl limit
max_crawl = 10

url_pattern = re.compile(r"/page/\d+/")
product_data = []

def crawler():
    pass
