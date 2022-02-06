# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

from Fake_Review_Detection.run import scrape


class AmazonscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    #Product_info
    product_name = scrapy.Field()
    brand = scrapy.Field()
    category = scrapy.Field()
    sub_category = scrapy.Field()
    price = scrapy.Field()
    mrp = scrapy.Field()
    return_policy = scrapy.Field()
    warranty = scrapy.Field()
    cod = scrapy.Field()
    fba = scrapy.Field()
    seller_url = scrapy.Field()
    avg_rating= scrapy.Field()
    one = scrapy.Field()
    two = scrapy.Field()
    three = scrapy.Field()
    four = scrapy.Field()
    five = scrapy.Field()
    total_ratings = scrapy.Field()
    total_reviews = scrapy.Field()
    asin_number = scrapy.Field()
    review_page = scrapy.Field()
    scraped_on = scrapy.Field()

class SellerscraperItem(scrapy.Item):
    seller_id = scrapy.Field()
    seller_name = scrapy.Field()
    pect_pos_rating = scrapy.Field()
    pect_neg_rating = scrapy.Field()
    pect_neu_rating = scrapy.Field()

class ReviewscraperItem(scrapy.Item):
    asin_number = scrapy.Field()
    review_id = scrapy.Field()
    user_name = scrapy.Field()
    user_link = scrapy.Field()
    rating = scrapy.Field()
    review_title = scrapy.Field()
    date = scrapy.Field()
    verified_purchase = scrapy.Field()
    review = scrapy.Field()
    helpful_count = scrapy.Field()

class UserscraperItem(scrapy.Item):
    user_id = scrapy.Field()
    user_name = scrapy.Field()
    total_helpful_votes = scrapy.Field()
    total_reviews = scrapy.Field()
