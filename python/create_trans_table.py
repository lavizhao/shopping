#coding: utf-8

import csv
from read_conf import config
import MySQLdb as mysql

conn = mysql.connect(host='localhost',user='root',passwd='111111111',port=3306)
cur = conn.cursor()

def create_db():

    count = cur.execute('create database if not exists shopping;')
    print "create database",count
    result = cur.fetchmany(count)
    print result
    conn.commit()

#cid代表用户的id
    
def create_trans_table():
    conn.select_db('shopping')
    cur = conn.cursor()
    count = cur.execute('create table trans (trans_id int primary key,cid varchar(40),chain varchar(40),dept varchar(40),category varchar(40),company varchar(40),brand varchar(40),date varchar(40),productsize varchar(40),productmeasure varchar(40),purchasequantity varchar(40),purchaseamount varchar(40)) ')
    print "create table train",count
    result = cur.fetchmany(count)
    print result
    conn.commit()

def insert_trans(conf):
    conn.select_db('shopping')        
    f = open(conf["reduction_trans_dir"])
    reader = csv.reader(f)

    a = 0
    for line in reader:
        row_string = '"'+str(a)+'","'+'","'.join(line)+'"'
        cur.execute('insert into trans values(%s);'%(row_string))
        a += 1
        if a % 10000 == 0 :
            conn.commit()
            print a
    conn.commit()

def drop_table():
    conn.select_db('shopping')
    cur = conn.cursor()
    count = cur.execute('drop table trans')
    print "drop table train",count
    result = cur.fetchmany(count)
    print result
    conn.commit()
            
#建索引 : create index cindex using btree on trans(cid);

def search_table(cid):
    conn.select_db('shopping')
    cur = conn.cursor()
    count = cur.execute('select * from trans where cid = "%s"'%(cid))
    result = cur.fetchmany(count)
    return result

def build_index():
    conn.select_db('shopping')
    cur = conn.cursor()
    count = cur.execute('create index cindex using btree on trans(cid);')
    result = cur.fetchmany(count)
    return result
    
    
if __name__ == '__main__':
    print "hello"

    data_position_conf = config("../conf/data_position.conf")
    drop_table()
    create_db()
    create_trans_table()
    insert_trans(data_position_conf)
    build_index()
    #result = search_table('86246')
    #print result[0]
