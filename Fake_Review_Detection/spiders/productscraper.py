import scrapy,re
from ..items import AmazonscraperItem
import json
import os
from datetime import date

with open(os.getcwd()+'\Fake_Review_Detection\config.json',"r") as f:
    pathfor = json.load(f)["pathfor"]

class ProductSpider(scrapy.Spider):
    name = "product_info"
    start_urls = []
    custom_settings = {
        'ITEM_PIPELINES': {'Fake_Review_Detection.pipelines.Productscraperpipeline': 300},
    }
    with open(pathfor["url.txt"]) as urllist:
        for url in urllist:
            start_urls.append(url)
       
    def productparse2(self, response):
            items = AmazonscraperItem()
            ratings_reviews = response.css('div.a-row.a-spacing-base.a-size-base span::text').extract()
            _date = str(date.today())


            # converting 6,840 global ratings | 1,755 global reviews to 6804,1755
            ratings_reviews = ratings_reviews[0].strip()
            ratings_reviews = ratings_reviews.split('|')
            items['total_ratings'] = str(ratings_reviews[0].split()[0]).replace(',','')
            items['total_reviews'] = str(ratings_reviews[1].split()[0]).replace(',','')
            items["product_name"] = response.request.meta['product_name']
            items["brand"] = response.request.meta['brand']
            items["category"] = response.request.meta['category']
            items["sub_category"] = response.request.meta['sub_category']
            items["price"] = response.request.meta['price']
            items["mrp"] = response.request.meta['mrp']
            items["fba"] = response.request.meta['fba']
            items["seller_url"] = response.request.meta['seller_url']
            items["avg_rating"] = response.request.meta['avg_rating']
            items["return_policy"] = response.request.meta['return_policy']
            items["warranty"] = response.request.meta['warranty']
            items["cod"] = response.request.meta['cod']
            items["one"] = response.request.meta['one']
            items["two"] = response.request.meta['two']
            items["three"] = response.request.meta['three']
            items["four"] = response.request.meta['four']
            items["five"] = response.request.meta['five']
            items['asin_number'] = response.request.meta['asin_number']
            items['review_page'] = response.request.url
            items['scraped_on'] = _date

            yield items


    def parse(self, response, **kwargs):
        items = AmazonscraperItem()
        product_name = response.css('span#productTitle::text').extract()
        brand = response.css('a#bylineInfo::text').extract()
        category = response.css('a.a-color-tertiary::text').extract()
        price = response.css('td.a-span12 span.a-size-medium ::text').extract()
        if(len(price)==0):
            price = response.css('span.a-price span.a-price-whole::text').extract()
        mrp = response.css('td.a-span12.a-color-secondary.a-size-base span.a-offscreen::text').extract()
        if(len(mrp)==0):
            mrp = response.css('span.a-price.a-text-price span.a-offscreen::text').extract()
        policies = response.css('a.a-size-small.a-link-normal.a-text-normal::text').extract()
        fba = response.css('span.a-icon-text-fba::text').extract()
        seller_url = response.css('div#merchant-info a::attr("href")').extract()
        avg_rating = response.css('span.a-nowrap.a-size-base span.a-size-medium.a-color-base::text').extract()
        pect_ratings = response.css('div.a-meter::attr("aria-valuenow")').extract()

        items['product_name'] = product_name[0].strip()
        items['brand'] = brand[0]
        try:
            items['category'] = category[0].strip()
        except:
            items['category'] = ""
        try:
            items['sub_category'] = category[-2].strip()
        except:
            items['sub_category'] = ""
        if(price[0].strip()[0] == "₹"):
            items['price'] = price[0].strip()[1:].replace(',','')
        else:
            items['price'] = price[0].strip().replace(',','')

        if(mrp[0].strip()[0] == "₹"):
            items['mrp'] = mrp[0].strip()[1:].replace(',','')
        else:
            items['mrp'] = mrp[0].strip().replace(',','')
        items['return_policy'] = 'No'
        items['warranty'] = 'No'
        items['cod'] = 'No'

        for i in policies:
            i = str(i)
            i.strip()
            if (i.find('Replacement') != -1 or i.find("Days Return") != -1):
                items['return_policy'] = 'Yes'
            if i.find("Warranty") != -1:
                items['warranty'] = 'Yes'
            if i.find('Pay') != -1:
                items['cod'] = 'Yes'

        if fba:
            items['fba'] = 'Yes'
        else:
            items['fba'] = 'No'

        items['seller_url'] = 'https://www.amazon.in/' + seller_url[0]

        avg_rating = avg_rating[0].split()
        items['avg_rating'] = avg_rating[0]

        items['one'] = pect_ratings[0].strip()[:-1]
        items['two'] = pect_ratings[1].strip()[:-1]
        items['three'] = pect_ratings[2].strip()[:-1]
        items['four'] = pect_ratings[3].strip()[:-1]
        items['five'] = pect_ratings[4].strip()[:-1]

        review_page = response.css('div#reviews-medley-footer a::attr(href)').extract()
        review_page = 'https://www.amazon.in' + review_page[0]

        asin_pattern = '[/]+[A-Z0-9]+[/?]'
        asin_number = re.search(asin_pattern, review_page)
        asin_number = asin_number.group()
        asin_number = asin_number[1:-1]
        items['asin_number'] = asin_number

        yield response.follow(review_page, callback=self.productparse2,
                              meta={'product_name': items['product_name'], 'brand': items['brand'],
                                    'category': items['category'],
                                    'sub_category': items['sub_category'], 'price': items['price'], 'mrp': items['mrp'],
                                    'return_policy': items['return_policy'], 'warranty': items['warranty'],
                                    'cod': items['cod'],
                                    'fba': items['fba'], 'seller_url': items['seller_url'],
                                    'avg_rating': items['avg_rating'],
                                    'one': items['one'], 'two': items['two'], 'three': items['three'],
                                    'four': items['four'],
                                    'five': items['five'], 'asin_number': items['asin_number']})




