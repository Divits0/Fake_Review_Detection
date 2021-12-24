from flask import Flask,render_template,request
from flask_pymongo import PyMongo
import re
from run import scrape
import os

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/Amazon_Data"
mongo = PyMongo(app)


def get_asin(url):
    asin_pattern = '[/]+[A-Z0-9]+[/?]'
    asin_number = re.search(asin_pattern,url)
    asin_number = asin_number.group()
    asin_number = asin_number[1:-1]
    return asin_number

def write_url(url):
    with open(r'C:\Users\jaish\Desktop\Project\Fake_Review_Detection\url.txt','w') as urllist:
        urllist.write(url)


@app.route("/get_url", methods = ['POST'])
def get_url():
    url = request.get_data()
    url = url.decode()
    write_url(url)
    asin_number = get_asin(url)
    product_colloection = mongo.db.product
    result = product_colloection.find_one({'asin_number': asin_number})
    print(result)
    if result is not None:
        print('inside if')
    else:
        print('hi')
        #os.system(r'cd C:\Users\jaish\Desktop\Project\Fake_Review_Detection\Fake_Review_Detection\Fake_Review_Detection')
        scrape()
    return ""
    

app.run(debug=True)