import scrapy,re
from ..items import AmazonscraperItem

class ProductSpider(scrapy.Spider):
    name = "product_info"
    start_urls = []
    custom_settings = {
        'ITEM_PIPELINES': {'Fake_Review_Detection.pipelines.Productscraperpipeline': 300},
    }
    with open(r'C:\Users\jaish\Desktop\Project\Fake_Review_Detection\Fake_Review_Detection\Fake_Review_Detection\url.txt') as urllist:
        i=0
        for each in urllist:
            start_urls.append(each)
            i+=1
            if i > 5:
                break
    def productparse2(self, response):
            items = AmazonscraperItem()
            ratings_reviews = response.css('div.a-row.a-spacing-base.a-size-base span::text').extract()


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

            yield items

    def parse(self, response, **kwargs):
        items = AmazonscraperItem()
        product_name = response.css('span#productTitle::text').extract()
        brand = response.css('a#bylineInfo::text').extract()
        category = response.css('a.a-color-tertiary::text').extract()
        price = response.css('td.a-span12 span.a-size-medium ::text').extract()
        mrp = response.css('td.a-span12.a-color-secondary.a-size-base span.a-offscreen::text').extract()
        policies = response.css('a.a-size-small.a-link-normal.a-text-normal::text').extract()
        fba = response.css('span.a-icon-text-fba::text').extract()
        seller_url = response.css('div#merchant-info a::attr("href")').extract()
        avg_rating = response.css('span.a-nowrap.a-size-base span.a-size-medium.a-color-base::text').extract()
        pect_ratings = response.css('td.a-nowrap a.a-link-normal::text').extract()

        items['product_name'] = product_name[0].strip()
        items['brand'] = brand[0]
        items['category'] = category[0].strip()
        items['sub_category'] = category[-2].strip()
        items['price'] = price[0][1:]
        items['mrp'] = mrp[0].strip()[1:]
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




