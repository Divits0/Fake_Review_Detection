import pymongo
import json
import os
with open(os.getcwd()+'\Fake_Review_Detection\config.json',"r") as f:
    pathfor = json.load(f)["pathfor"]
def calculate(asin_number):
    client = pymongo.MongoClient(pathfor["db_URI"])
    db = client["Amazon_Data"]
    product_collection = db["product"]
    feedback_collection = db["feedback"]
    x = product_collection.find_one({'asin_number': asin_number})
    y = feedback_collection.find_one({'asin_number': asin_number})


    def feedback_protocol(x,y,impact,model_score):
        if x["asin_number"] == y["asin_number"]:
            last_feedback = int(y["last_feedback"])
            pos = int(y["positive"])
            neg = int(y["negative"])
            accuracy  = (model_score/35)*100
            if not last_feedback:
                if neg > pos:
                    diff = neg - pos
                    delta = diff*0.1 + impact*0.1
                    if accuracy < 45:
                        final = model_score + delta
                        return final
                    if accuracy > 55:
                        final = model_score - delta
                        return final
        return model_score


    def cal_discount(pr,mrp):
        pr = float(pr)
        mrp = float(mrp)
        dis = (1 - pr/mrp)*100
        return dis

    def price_score(price):
        price = float(price)
        if price < 1500:
            return 'cheap'
        elif price > 1500 and price < 5000:
            return 'medium'
        return 'costly'

    def discount_score(discount):
        if discount < 33:
            return 'less'
        return 'more'

    def review_length_score(review_length):
        if review_length < 30:
            return 'low'
        elif review_length > 30 and review_length < 200:
            return 'normal'
        return 'high'

    def rating_score(rating):
        rating = float(rating)
        if rating < 3:
            return 'low'
        elif rating == 3:
            return 'average'
        return 'high'

    data = {'category': x["category"], 'price': x["price"], 'discount': cal_discount(x["price"],x["mrp"]), 'return_policy': x["return_policy"], 'warranty': x["warranty"], 'cod': x["cod"], 'rating': x["avg_rating"], 'fulfilled': x["fba"]}
    print(data)

    #category = (2.765, 3.245, 1.435, 2.82, 2.98, 0.69, 4.2, 2.18, 1.755)
    price = (2.605, 1.7, 0.695)
    discount = (0.53, 4.47)
    return_policy = (3.83, 1.17)
    warranty = (3.885, 1.115)
    cod = (3.83, 1.17)
    #review_length = (1.6775, 1.7, 1.6225)
    rating = (1.3575, 1.385, 2.2575)
    #helpful_count = (2.235, 2.765)
    fulfilled = (3.725, 1.275)

    #category_data = {'electronics': 0, 'fashion': 1, 'home': 2, 'automobile': 3, 'music': 4, 'books': 5, 'beauty': 6, 'sports': 7, 'toys': 8}
    price_data = {'cheap': 0, 'medium': 1, 'costly': 2}
    discount_data = {'less': 0, 'more': 1}
    return_policy_data = {'no': 0, 'yes': 1}
    warranty_data = {'no': 0, 'yes': 1}
    cod_data = {'no': 0, 'yes': 1}
    #review_length_data = {'low': 0, 'normal': 1, 'high': 2}
    rating_data = {'low': 0, 'average': 1, 'high': 2}
    #helpful_count_data = {'no': 0, 'yes': 1} #note: model depends upon the count of helpful votes
    fulfilled_data = {'no': 0, 'yes': 1}

    overall_score = 35

    # model_score += category[category_data[data['category']]]
    pr_score = price[price_data[price_score(data['price'])]]
    dis_score = discount[discount_data[discount_score(data['discount'])]]
    rp_score = return_policy[return_policy_data[data['return_policy'].lower()]]
    war_score = warranty[warranty_data[data['warranty'].lower()]]
    cod_score = cod[cod_data[data['cod'].lower()]]
    #rl_score = review_length[review_length_data[review_length_score(data['review_length'])]]
    rat_score = rating[rating_data[rating_score(data['rating'])]]
    #hc_score = helpful_count[helpful_count_data[data['helpful_count']]]
    fba_score = fulfilled[fulfilled_data[data['fulfilled'].lower()]]

    model_score = pr_score + dis_score + rp_score + war_score + cod_score + rat_score + fba_score
    impact = max(pr_score,dis_score,rp_score,war_score,cod_score,rat_score,fba_score)
    
    if(y["prev_score"] != -1):
        model_score = feedback_protocol(x,y,impact,y["prev_score"])

    feedback_collection.update_one({'asin_number':asin_number}, {"$set": {"prev_score": model_score}})
    accuracy = model_score/overall_score*100
    print(accuracy)
    if accuracy < 45:
        return "Less Likely to have Fake reviews"
    elif accuracy > 45 and accuracy < 55:
        return "Moderately Likely to have Fake reviews"
    else:
        return "More Likely to have Fake reviews"
