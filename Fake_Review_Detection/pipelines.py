# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
class AmazonscraperPipeline:
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item

class Productscraperpipeline(object):
    def __init__(self):
        self.conn = pymongo.MongoClient('localhost',27017)
        db = self.conn['Amazon_Data']
        self.collection = db['product']

    def process_item(self, item, spider):
        self.collection.insert_one(dict(item))
        return item

class Sellerscraperpipeline(object):
    def __init__(self):
        self.conn = pymongo.MongoClient('localhost',27017)
        db = self.conn['Amazon_Data']
        self.collection = db['seller']

    def process_item(self, item, spider):
        self.collection.insert_one(dict(item))
        return item

class Reviewscraperpipeline(object):
    def __init__(self):
        self.conn = pymongo.MongoClient('localhost',27017)
        db = self.conn['Amazon_Data']
        self.collection = db['review']

    def process_item(self, item, spider):
        self.collection.insert_one(dict(item))
        return item
