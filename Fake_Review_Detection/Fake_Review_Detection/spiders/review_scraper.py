import scrapy,re
import json
from word2number import w2n
from ..items import ReviewscraperItem

class ReviewSpider(scrapy.Spider):
    name = 'review_info'
    start_urls = []

    custom_settings = {
        'ITEM_PIPELINES': {'Fake_Review_Detection.pipelines.Reviewscraperpipeline': 300},
    }
    with open(r'C:\Users\jaish\Desktop\Project\Fake_Review_Detection\Fake_Review_Detection\Fake_Review_Detection\product_info.json','r') as product_info:

        try:
            data = json.load(product_info)
            for each in data:
                start_urls.append(each['review_page'])
        except:
            pass

    def parse(self, response, **kwargs):
        items = ReviewscraperItem()
        id = response.css('div#cm_cr-review_list div.a-section.review.aok-relative::attr("id")').extract()
        for i in id:
            user_name = response.css('div#'+i+' span.a-profile-name::text').extract()
            user_link = response.css('div#'+i+' a.a-profile::attr("href")').extract()
            rating = response.css('div#'+i+' a.a-link-normal::attr("title")').extract()
            review_title = response.css('div#'+i+' a.a-text-bold span::text').extract()
            date = response.css('div#'+i+' span.review-date::text').extract()
            verified_purchase = response.css('div#'+i+' span.a-color-state::text').extract()
            review = response.css('div#'+i+' span.review-text-content span::text').extract()
            helpful_count = response.css('div#'+i+' span.cr-vote-text::text').extract()

            asin_pattern = '[/]+[A-Z0-9]+[/?]'
            asin_number = re.search(asin_pattern, response.url)
            asin_number = asin_number.group()
            asin_number = asin_number[1:-1]
            items['asin_number'] = asin_number

            items['review_id'] = i
            items['user_name'] = user_name[0]
            items['user_link'] = 'amazon.in'+user_link[0]
            items['rating'] = rating[0].split()[0]
            items['review_title'] = review_title[0]
            items['date'] = " ".join(date[0].split()[-3:])
            try:
                items['verified_purchase'] = verified_purchase[0]
            except:
                items['verified_purchase'] = ''
            items['review'] = ' '.join(review).strip()
            try:
                items['helpful_count'] = w2n.word_to_num(helpful_count[0].split()[0])
            except:
                items['helpful_count'] = 0

            yield items

        # next_page = response.css('li.a-last a::attr(href)').get()
        # if next_page is not None:
        #     yield response.follow(next_page, callback=self.parse)