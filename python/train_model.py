#coding: utf-8

import csv
from read_conf import config
from sklearn.linear_model import LogisticRegression
from sklearn import cross_validation
import numpy as np
import sys
from sklearn.naive_bayes import GaussianNB
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.ensemble import GradientBoostingClassifier

def read_data(conf):
    #read train test y

    train,test,y,test_label = [],[],[],[]

    f = open(conf["train_dir"])
    reader = csv.reader(f)
    for line in reader:
        sub_line = line[1:]
        sub_line = [float(i) for i in sub_line]
        train.append(sub_line)

    f.close()

    f = open(conf["test_dir"])
    reader = csv.reader(f)
    for line in reader:
        test_label.append(line[0])
        sub_line = line[1:]
        sub_line = [float(i) for i in sub_line]
        test.append(sub_line)

    f.close()
        
    f = open(conf["y_dir"])
    reader = csv.reader(f)
    for line in reader:
        y.append(float(line[0]))

    f.close()
    return train,test,y,test_label
    
def train_by_lr(conf,ctype):
    """
    
    Arguments:
    - `conf`:
    """
    #read train test y
    print "load data..."
    train,test,y,test_label = read_data(conf)
    train,test,y = np.array(train),np.array(test),np.array(y)

    #print "norm"
    #scaler = preprocessing.StandardScaler().fit(train)
    #train = scaler.transform(train)
    #test = scaler.transform(test)
    
    #clf = LogisticRegression(penalty='l2',dual=True,fit_intercept=False,C=2,tol=1e-9,class_weight=None, random_state=None, intercept_scaling=1.0)
    clf = GaussianNB()
    #clf = GradientBoostingClassifier(n_estimators=400)
    #clf = RandomForestClassifier(n_estimators=40)
    #clf = SGDClassifier(loss="log", penalty="l2",alpha=0.1)
    if ctype == "cv":
        print "交叉验证"
        hehe = cross_validation.cross_val_score(clf,train,y,cv=3,scoring='roc_auc',n_jobs=3)
        print hehe
        print np.mean(hehe)

    elif ctype =="predict":
        clf.fit(train,y)
        predict = clf.predict_proba(test)[:,1]

        if len(predict)!=len(test_label):
            print "predict!=test label"
            sys.exit(1)

        rf = open(conf["result_dir"],"w")
        rf.write("id,repeatProbability\n")
        for i in range(len(predict)):
            rf.write("%s,%s\n"%(test_label[i],predict[i]))


if __name__ == '__main__':
    print "hello"
    data_position_conf = config("../conf/data_position.conf")

    train_by_lr(data_position_conf,"predict")
    #train_by_lr(data_position_conf,"cv")
