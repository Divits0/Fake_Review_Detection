import os,json
import touch

with open(os.getcwd()+'\Fake_Review_Detection\config.json',"r") as f:
    pathfor = json.load(f)["pathfor"]

def scrape():
    os.system('del product_info.json')
    os.system('del seller_info.json')
    os.system('del review_info.json')
    touch.touch(os.getcwd()+'\\product_info.json')
    touch.touch(os.getcwd()+'\\seller_info.json')
    touch.touch(os.getcwd()+'\\review_info.json')
    try:
        for i in range(3):
            os.system('scrapy crawl product_info -o product_info.json')
            if os.stat(pathfor["product_info"]).st_size != 0:
                break   
            print("_________________________RETRYING #",i+1)
        else:
            return False     
    except:
        print('__________________product')
        return False
    
    try:
        for i in range(3):
            os.system('scrapy crawl seller_info -o seller_info.json')
            if os.stat(pathfor["seller_info"]).st_size != 0:
                break  
        else:
            return False   
    except:
        print('__________________seller')
        return False
    try:
        for i in range(3):
            os.system('scrapy crawl review_info -o review_info.json')
            if os.stat(pathfor["review_info"]).st_size != 0:
                break  
        else:
            return False   
    except:
        print('__________________review')
        return False
    return True
