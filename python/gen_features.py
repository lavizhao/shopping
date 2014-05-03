#coding: utf-8
'''
根据数据文件产生特征，重新生成测试、训练集
'''

from read_conf import config
import csv,sys
import create_trans_table
from create_trans_table import *
from datetime import datetime, date

################################
#定义个offer类，到时侯方便用
#在查看用户购买offer的历史记录时，可以查找到具体品牌等信息
class offer:
    def __init__(self,line):
        self.offer_id = line[0]
        self.category = line[1]
        self.quantity = line[2]
        self.company = line[3]
        self.offer_value = line[4]
        self.brand = line[5]

    def __str__(self):
        return 'offer_id: '+self.offer_id+"\ncategory: "+self.category+\
            "\nquantity: "+self.quantity+"\ncompany: "+self.company+\
            "\noffer_value: "+self.offer_value+"\nbrand: "+self.brand
        
def read_offer(conf):
    offers = {}        
    f = open(conf["offer_dir"])        
    reader = csv.reader(f)
    a = 0
    for line in reader:
        if a == 0:
            a += 1
            continue
        #hehe
        offers[line[0]] = offer(line)

    return offers
###############################

#定义customer类，也就相当于用户的profile，在train和test中，我都看了，没有重复的，可以用作字典

class customer:
    def __init__(self,cid,bought_company_times,bought_brand_times,bought_category_times,offer_value,quantity,\
                 bought_company_quantity,bought_company_amount,bought_category_quantity,bought_category_amount,\
                 bought_company_category,bought_company_brand,bought_brand_category,bought_company_category_brand,\
                 bought_company_30,bought_company_60,bought_company_90):
        self.id = cid
        self.bought_company_times = bought_company_times
        self.bought_brand_times = bought_brand_times
        self.bought_category_times = bought_category_times
        self.offer_value = offer_value
        self.quantity = quantity
        self.bought_company_quantity = bought_company_quantity
        self.bought_company_amount = bought_company_amount
        self.bought_category_quantity = bought_category_quantity
        self.bought_category_amount = bought_category_amount
        self.bought_company_category = bought_company_category
        self.bought_company_brand = bought_company_brand
        self.bought_brand_category = bought_brand_category
        self.bought_company_category_brand = bought_company_category_brand
        self.bought_company_30 = bought_company_30
        self.bought_company_60 = bought_company_60
        self.bought_company_90 = bought_company_90

        self.never_bought_category = self.judge_never_bought(bought_category_times)
        self.never_bought_company = self.judge_never_bought(bought_company_times)
        self.never_bought_brand = self.judge_never_bought(bought_brand_times)
        self.never_bought_3 = self.judge_never_bought(bought_company_category_brand)
        
    def judge_never_bought(self,num):
        if num != 0:
            return num
        else:
            return 0
        
    def __str__(self):

        return "id: "+self.id

    def feature_string(self):
        #return "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s"\
        #    %(self.id,self.bought_company_times,self.bought_brand_times,self.bought_category_times,self.offer_value,self.quantity\
        #      ,self.bought_company_quantity,self.bought_company_amount,self.bought_category_quantity,self.bought_category_amount,\
        #      self.bought_company_category,self.bought_company_brand,self.bought_brand_category,\
        #      self.never_bought_category,self.never_bought_company,self.never_bought_brand,self.bought_company_category_brand)

        return "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s"\
            %(self.id,self.bought_company_times,self.bought_brand_times,self.bought_category_times,self.offer_value,\
              self.bought_company_category,self.bought_company_brand,self.bought_brand_category,\
              self.never_bought_category,self.never_bought_company,self.never_bought_brand,self.bought_company_category_brand,self.never_bought_3,\
              self.bought_company_30,self.bought_company_60,self.bought_company_90)


def customer_string(feature_string):
    feature_string = [str(i) for i in feature_string]
    return ','.join(feature_string)

def diff_days(s1,s2):
    date_format = "%Y-%m-%d"
    a = datetime.strptime(s1, date_format)
    b = datetime.strptime(s2, date_format)
    delta = b - a
    return delta.days

def get_weekday(day):
    date_format = "%Y-%m-%d"
    s_day = datetime.strptime(day, date_format)
    return s_day.isoweekday()
        
#先给每个用户建一个空类
#ctype 代表数据集种类，train，test两种
#最后返回的是一个字典，每个键值是客户的id
def get_customer_class(conf,ctype,offers):

    customers = []
    if ctype == "train":
        f = open(conf["train_history_dir"])
        t = open(conf["train_dir"],"w")
        y = []
        r = open(conf["y_dir"],"w")
    elif ctype == "test":
        f = open(conf["test_history_dir"])
        t = open(conf["test_dir"],"w")
    else :
        print "no such file"
        sys.exit(1)

    reader = csv.reader(f)
    a = 0
    for line in reader:
        if a == 0:
            a += 1
        else:
            if ctype == "train":
                if line[5]=="t":
                    y.append(1)
                elif line[5]=="f":
                    y.append(0)
                else:
                    print "error"
                    sys.exit(1)
            cid = line[0]
            offer_id = line[2]

            this_offer = offers[offer_id]

            customer_date = line[-1]
            
            #返回从mysql中的查询结果
            result = search_table(cid)

            #feature 1: 用户买过几次这个company的商品
            #feature 6: 用户买过这个company的quantity
            #feature 7: 用户买过这个company的amount
            bought_company_times = 0
            bought_company_amount = 0
            bought_company_quantity = 0
            company_id = this_offer.company

            #feature 2: 用户买过几次这个brand的商品
            bought_brand_times = 0
            brand_id = this_offer.brand
            

            #feature 3:用户买过几次这个category的商品
            #feature 8: 用户买过这个company的quantity
            #feature 9: 用户买过这个company的amount
            bought_category_times = 0
            category_id = this_offer.category
            bought_category_amount = 0
            bought_category_quantity = 0

            #feature 10 : 用户既买过这个company又买过这个category
            bought_company_category = 0
            #feature 11 : 用户既买过这个company又买过这个brand
            bought_company_brand = 0
            #feature 12 : 用户既买过这个brand又买过这个category
            bought_brand_category = 0
            #feature 13 : 都买过三类
            bought_company_category_brand = 0

            #feature 27 : 买过这个company且日期小于5天的
            bought_category_5 = 0
            #feature 28 : 买过这个company且日期小于15天的
            bought_category_15 = 0
            #feature 14 : 买过这个company且日期小于30天的
            bought_category_30 = 0
            #feature 15 : 买过这个company 小于60的
            bought_category_60 = 0
            #feature 16 : 买过 小于  90的
            bought_category_90 = 0
            #feature 17 : 小于120的
            bought_category_120 = 0

            #feature 19 :买过这个company且日期小于30天的
            bought_company_30 = 0

            #feature 20 :总共的购买记录
            #if len(result) > 300:
            #    total_bought = 1
            #else:
            #    total_bought = 0

            #feature 27 : .... 小于0的
            bought_company_category_brand_0 = 0
            #feature 30 : 小于 1的
            bought_company_category_brand_1 = 0
            #feature 21 : ... 5
            bought_company_category_brand_5 = 0
            #feature 28 : .... 小于10的
            bought_company_category_brand_10 = 0
            #feature 22 :买过这个company category brand 且日期小于15天的
            bought_company_category_brand_15 = 0
            #feature 23 :买过这个company category brand 且日期小于30天的
            bought_company_category_brand_30 = 0
            #feature 24 :....                                    60
            bought_company_category_brand_60 = 0
            #feature 25 :  90
            bought_company_category_brand_90 = 0
            #feature 26 :  120
            bought_company_category_brand_120 = 0

            #feature 31 : 买过这个category brand且日期小于10天的
            bought_brand_category_10 = 0

            #feature 29 :平均花钱数目
            avg_amount = 0
            
            #feature 32:关于周末
            bought_in_weekend = 0
            bought_in_weekday = 0
            #get_offer_in_weekend = 0
            
            for one_search in result:
                date_diff_days = diff_days(one_search[7],customer_date)
                avg_amount += float(one_search[-1])

                if one_search[5] == company_id :
                    bought_company_times += 1
                    bought_company_quantity += float(one_search[10])
                    bought_company_amount += float(one_search[11])
                    #if date_diff_days < 30 :
                    #    bought_company_30 += 1

                
                if one_search[6] == brand_id:
                    bought_brand_times += 1

                if one_search[4] == category_id:
                    bought_category_times += 1
                    #bought_category_quantity += float(one_search[10])
                    #bought_category_amount += float(one_search[11])
                    if date_diff_days < 5:
                        bought_category_5 += 1
                    elif date_diff_days < 15:
                        bought_category_15 += 1
                    elif date_diff_days < 30:
                        bought_category_30 += 1
                    elif date_diff_days < 60:
                        bought_category_60 += 1
                    elif date_diff_days < 90:
                        bought_category_90 += 1
                    elif date_diff_days < 120:
                        bought_category_120 += 1


                if one_search[4]==category_id and one_search[5] == company_id:
                    bought_company_category += 1

                if one_search[5] == company_id and one_search[6] == brand_id:
                    bought_company_brand += 1

                if one_search[4] == category_id and one_search[6] == brand_id:
                    bought_brand_category += 1

                if one_search[4] == category_id and one_search[5] == company_id and one_search[6] == brand_id:
                    bought_company_category_brand += 1
                    if date_diff_days < 1:
                        bought_company_category_brand_1 += 1
                    elif date_diff_days < 5:
                        bought_company_category_brand_5 += 1
                    elif date_diff_days < 10:
                        bought_company_category_brand_10 += 1
                    elif date_diff_days < 15:
                        bought_company_category_brand_15 += 1
                    elif date_diff_days < 30:
                        bought_company_category_brand_30 += 1
                    elif date_diff_days < 60:
                        bought_company_category_brand_60 += 1
                    elif date_diff_days < 90:
                        bought_company_category_brand_90 += 1
                    elif date_diff_days < 120:
                        bought_company_category_brand_120 += 1

            #avg_amount /= (len(result)+1)
                
                weekday = get_weekday(one_search[7])
                if weekday == 6 or weekday == 7:
                    bought_in_weekend += 1
                if weekday != 6 and weekday != 7:
                    bought_in_weekday += 1
                    
                #temp_offer_day = get_weekday(customer_date)
                #if temp_offer_day == 5 or temp_offer_day == 6 or temp_offer_day == 7 :
                #    get_offer_in_weekend += 1
            #feature 4,5: offer value offer quantity
                    
            #this_customer = customer(cid,bought_company_times,bought_brand_times,bought_category_times,this_offer.offer_value,this_offer.quantity,bought_company_quantity\
            #                         ,bought_company_amount,bought_category_quantity,bought_category_quantity,bought_company_category,bought_company_brand,\
            #                         bought_brand_category,bought_company_category_brand,bought_company_30,bought_company_60,bought_company_90)
            #customers.append(this_customer)
            t.write(customer_string(\
                                    [cid,bought_company_times,bought_brand_times,bought_category_times,this_offer.offer_value,\
                                     bought_company_category,bought_company_brand,\
                                     bought_brand_category,bought_company_category_brand,bought_category_5,bought_category_15,\
                                     bought_category_30,bought_category_60,bought_category_90,bought_category_120,\
                                     bought_company_category_brand_1,\
                                     bought_company_category_brand_5,bought_company_category_brand_10,bought_company_category_brand_15,\
                                     bought_company_category_brand_30,bought_company_category_brand_60,\
                                     bought_company_category_brand_90,bought_company_category_brand_120,\
                                     bought_in_weekend,bought_in_weekday\
                                 ])+"\n")
            #,get_offer_in_weekend\
            a += 1
            if a % 10000 == 0:
                print a

    #for this_customer in customers:
    #    t.write(this_customer.feature_string()+"\n")
    if ctype == "train":
        for ty in y:
            r.write("%s\n"%(ty))
    return customers
    

if __name__ == '__main__':
    print "hello"
    data_position_conf = config("../conf/data_position.conf")
    offers = read_offer(data_position_conf)

    customers = get_customer_class(data_position_conf,"train",offers)
    tcustomers = get_customer_class(data_position_conf,"test",offers)

    


