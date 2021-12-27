import scrapy
import re,json
from csv import reader
from ..items import SellerscraperItem
import os

with open(os.getcwd()+'\Fake_Review_Detection\config.json',"r") as f:
    pathfor = json.load(f)["pathfor"]

class SellerSpider(scrapy.Spider):
    name = 'seller_info'
    start_urls = []
    custom_settings = {
        'ITEM_PIPELINES': {'Fake_Review_Detection.pipelines.Sellerscraperpipeline': 300},
    }
    with open(pathfor["product_info"],'r') as product_info:

        try:
            data = json.load(product_info)
            for each in data:
                start_urls.append(each['seller_url'])
        except:
            pass

    def parse(self,response,**kwargs):
        items = SellerscraperItem()

        seller_id_pattern = '[=]+[A-Z0-9]*'
        seller_id = re.findall(seller_id_pattern, response.url)
        seller_id = seller_id[1]
        seller_id = seller_id[1:]


        seller_name = response.css('h1#sellerName::text').extract()
        pect_pos_rating = response.css('td.a-text-right span.a-color-success::text').extract()
        pect_neu_rating = response.css('td.a-text-right span.a-color-secondary::text').extract()
        pect_neg_rating = response.css('td.a-text-right span.a-color-error::text').extract()

        items['seller_id'] = seller_id
        items['seller_name'] = seller_name[0]
        items['pect_pos_rating'] = pect_pos_rating[-1]
        items['pect_neu_rating'] = pect_neu_rating[-1]
        items['pect_neg_rating'] = pect_neg_rating[-1]

        yield items









