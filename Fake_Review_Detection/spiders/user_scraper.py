import scrapy,re
import json
from ..items import UserscraperItem

class UserSpider(scrapy.Spider):
    name = 'user_info'
    start_urls = ['https://www.amazon.in/gp/profile/amzn1.account.AEF7WL7QS5CYKDH6AX6I4RQ6ZJPA/ref=cm_cr_dp_d_gw_tr?ie=UTF8']
    # with open(r'C:\Users\jaish\Desktop\Project\Web Scraping\Scrapy\amazonscraper\amazonscraper\review_info.json.','r') as product_info:
    #
    #     try:
    #         data = json.load(product_info)
    #         for each in data:
    #             start_urls.append(each['user_link'])
    #     except:
    #         pass

    def parse(self, response, **kwargs):
        items = UserscraperItem()

        user_name = response.css('span.a-size-extra-large::text').extract()
        a = response.css('div#profile_v5 span.a-size-large::text').extract()
        pattern = '/Aa-size-extra-large'
        res = re.findall(pattern,response.text)
        print(res)

        items['user_name'] = user_name

        # pattern = '[.]+[A-Z0-9]+[/?]'
        # user_id = re.search(pattern, response.url)
        # user_id = user_id.group()
        # user_id = user_id[1:-1]
        # items['user_id'] = user_id

        yield items