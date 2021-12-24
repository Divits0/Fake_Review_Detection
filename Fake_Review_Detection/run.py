#this is a comment
import os
from time import process_time_ns

def scrape():
    os.system('del product_info.json')
    os.system('del seller_info.json')
    os.system('del review_info.json')
    os.system('touch product_info.json')
    os.system('touch seller_info.json')
    os.system('touch review_info.json')
    try:
        os.system('scrapy crawl product_info -o product_info.json')
    except:
        print("___________________product")
    try:
        os.system('scrapy crawl seller_info -o seller_info.json')
    except:
        print('__________________seller')
    try:
        os.system('scrapy crawl review_info -o review_info.json')
    except:
        print('__________________review')
#scrape('')

