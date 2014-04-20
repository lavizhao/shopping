# coding: utf-8

import csv
from read_conf import config
import sys

#company,brand,category
def extract_offer(conf):
    f = open(conf["offer_dir"])
    company,brand,category = [],[],[]
    reader = csv.reader(f)
    
    a = 0
    for line in reader:
        if a == 0:
            a += 1
            continue
        category.append(line[1])
        company.append(line[3])
        brand.append(line[5])

    return [category,company,brand]

#抽取出所有campany，brand，category，留做选取feature用
def reduct_transactions(conf,offer):
    category,company,brand = offer[0],offer[1],offer[2]
    category,company,brand = set(category),set(company),set(brand)
        
    s = open(conf["trans_dir"])
    t = open(conf["reduction_trans_dir"],"w")
    reader = csv.reader(s)
    a = 0

    for line in reader:
        if a == 0:
            a += 1
            continue

        if line[3] in category or line[4] in company or line[5] in brand:
            write_str = ','.join(line)
            t.write(write_str+"\n")
            
        if a % 10000 == 0:
            print a    
        a += 1
    
    
if __name__ == '__main__':
    print "hello"
    data_position_conf = config("../conf/data_position.conf")

    offer = extract_offer(data_position_conf)
    reduct_transactions(data_position_conf,offer)



    

