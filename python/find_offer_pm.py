#coding: utf-8
'''
连接offer和transection两个文件，找到offer的productmeasure
'''

from read_conf import config
import csv,sys
from create_trans_table import *

if __name__ == '__main__':
    data_position_conf = config("../conf/data_position.conf")
    of = open(data_position_conf["offer_dir"],"r")
    rf = open(data_position_conf["offer_pm_dir"],"w")

    reader = csv.reader(of)
    writer = csv.writer(rf)
    count = 0

    for line in reader:
        if count == 0:
            count += 1
            line.append('productmeasure')
            writer.writerow(line)
        else:
            line.append(search_table_with_ccb(line[1],line[3],line[5]))
            writer.writerow(line)
            print count
            count += 1
            
    of.close()
    rf.close()
