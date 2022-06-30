from flask import Flask,render_template,request
from flask_pymongo import PyMongo
import re
from pymongo import database
from run import scrape
import json
import os
import ml_model

with open(os.getcwd()+'\Fake_Review_Detection\config.json',"r") as f:
    pathfor = json.load(f)["pathfor"]
asin_number = ""

app = Flask(__name__)
app.config["MONGO_URI"] = pathfor["db_URI"]
mongo = PyMongo(app)

def get_asin(url):
    asin_pattern = '[/]+[A-Z0-9]+[/?]'
    asin_number = re.search(asin_pattern,url)
    asin_number = asin_number.group()
    asin_number = asin_number[1:-1]
    return asin_number

def write_url(url):
    with open(pathfor["url.txt"],'w') as urllist:
        urllist.write(url)


@app.route("/get_feedback", methods = ['POST'])
def get_feedback():
    user_feedback = request.get_data()
    user_feedback = int(user_feedback.decode())
    global asin_number
    feedback_collection = mongo.db.feedback
    result = feedback_collection.find_one({'asin_number':asin_number})
    new_negative = result['negative']
    new_positive = result['positive']
    print(user_feedback,new_positive,new_negative) 
    if user_feedback:
        new_positive += 1
    else:
        new_negative += 1 
    print(user_feedback,new_positive,new_negative)    
    feedback_collection.update_one({'asin_number':asin_number}, {"$set": {"positive": new_positive, "negative": new_negative, "last_feedback": user_feedback}})
    return ""

@app.route("/get_url", methods = ['POST'])
def get_url():
    url = request.get_data()
    url = url.decode()
    write_url(url)
    global asin_number
    try:
        asin_number = get_asin(url)
    except:
        return 'Please make sure the pre-requisites are met, otherwise try again later'
    product_colloection = mongo.db.product
    review_collection = mongo.db.review
    result = product_colloection.find_one({'asin_number': asin_number})
    print(asin_number, result,"---------------------------------------")
    if result is not None:
        try:
            res = ml_model.calculate(asin_number)
            return res
        except:
            return 'Please make sure the pre-requisites are met, otherwise try again later'
    else:
        mongo.db['feedback'].insert_one({"asin_number":asin_number,"positive":0,"negative":0,"last_feedback":1, "prev_score": -1})
        #os.system(r'cd C:\Users\jaish\Desktop\Project\Fake_Review_Detection\Fake_Review_Detection\Fake_Review_Detection')
        success = scrape()
        print("____________ Scraped _____________ : ",success)
        if success == False:
            return 'Please make sure the pre-requisites are met, otherwise try again later'
    try:
        res = ml_model.calculate(asin_number)
        return res
    except: 
        return 'Please make sure the pre-requisites are met, otherwise try again later'
    

app.run(debug=True)