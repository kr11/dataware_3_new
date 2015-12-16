__author__ = 'KangRong'

from preprocessing.preprocessing import *
import time

def test_k_fold_cross_validation_plus(data,labels,k,func,classify):
    label_value_types = get_all_value({},data,labels)
    start = time.clock()
    n = len(data)
    itv = n/k
    step = [i * itv for i in range(0,k)]
    step.append(-1)
    total_right = 0
    bayes_model = []
    start = time.clock()
    for i in range(0,k):
        print("fold:{0}").format(i)
        bayes_model.append(func(data[0:step[i]]+data[step[i+1]:-1],labels.copy(),label_value_types))
    end = time.clock()
    print "build 10 model:read:%.2f s"% (end - start)

    for i in range(0,k):
        right = 0
        wrong = 0
        for item in data[step[i]:step[i+1]]:
        #for item in data[0:4000]:
            res = [classify(bayes_model[s], labels,item) for s in range(k)]
            re = '"no"' if (res.count('"no"')>res.count('"yes"')) else '"yes"'
            if re == item['class']:
                right += 1
            else:
                wrong += 1
        print "right:"+str(right)+";wrong:"+str(wrong)+";"+"rate;"+str(float(right*100)/(wrong+right))
        total_right += right
    print("total right:{0},total count:{1};rate;{2}").format(total_right,n,float(total_right)/n)
    end = time.clock()
    print "read:%.2f s"% (end - start)
    return total_right
    #print step


def test_k_fold_cross_validation_packet(data,labels,k,func,classify):
    label_value_types = get_all_value({},data,labels)
    start = time.clock()
    n = len(data)
    itv = n/k
    step = [i * itv for i in range(0,k)]
    step.append(-1)
    total_right = 0
    bayes_model = []
    start = time.clock()
    for i in range(0,k):
        print("fold:{0}").format(i)
        bayes_model.append(func(data[step[i]:step[i+1]], labels.copy(),label_value_types))
    end = time.clock()
    print "build 10 model:read:%.2f s"% (end - start)

    for i in range(0,k):
        right = 0
        wrong = 0
        for item in data[step[i]:step[i+1]]:
        #for item in data[0:4000]:
            res = []
            for s in range(k):
                if s != i:
                    res.append(classify(bayes_model[s], labels,item))
            re = '"no"' if (res.count('"no"')>res.count('"yes"')) else '"yes"'
            if re == item['class']:
                right += 1
            else:
                wrong += 1
        print "right:"+str(right)+";wrong:"+str(wrong)+";"+"rate;"+str(float(right*100)/(wrong+right))
        total_right += right
    print("total right:{0},total count:{1};rate;{2}").format(total_right,n,float(total_right)/n)
    end = time.clock()
    print "read:%.2f s"% (end - start)
    return total_right
    #print step

def test_del_multi_labels(labels,data,func,classify,delete_label):
    test_labels = ["euribor3m","emp.var.rate","nr.employed","campaign","cons.price.idx","contact","loan"
    ,"housing","marital","education","default","cons.conf.idx","job","age","poutcome","month","previous","duration","pdays"
               ]
    #temp = sys.stdout
    n = len(data)
    #for i in range(1,len(test_labels)):
    temp_labels = labels.copy()
    #del(temp_labels["pdays"])
    #del(temp_labels["duration"])
    for s in range(delete_label):
        del temp_labels[test_labels[s]]
    #temp_labels = {}
    #temp_labels["pdays"] =labels["pdays"]
    #temp_labels["duration"] =labels["duration"]

    #total_right = test_k_fold_cross_validation_plus(data,temp_labels.copy(),10,func,classify)
    total_right = test_k_fold_cross_validation_packet(data,temp_labels.copy(),10,func,classify)
    #total_right = test_k_fold_cross_validation(data,temp_labels.copy(),10,func,classify)
    #sys.stdout.close()
    #draw_histogram(label,data)
    #sys.stdout = temp
    print("delete first {0} labels").format(delete_label),
    print("total right:{0},total count:{1};rate:{2}").format(total_right,n,float(total_right)/n)

def test_k_fold_cross_validation(data,labels,k,func,classify):
    label_value_types = get_all_value({},data,labels)
    start = time.clock()
    n = len(data)
    itv = n/k
    step = [i * itv for i in range(0,k)]
    step.append(-1)
    total_right = 0
    build_total = 0
    bayes_model = []
    for i in range(0,k):
        #print("fold:{0}").format(i)
        start_build = time.clock()
        m_tree = func(data[0:step[i]]+data[step[i+1]:-1],labels.copy(),label_value_types)
        bayes_model.append(m_tree)
        end_build = time.clock()
        build_total += end_build-start_build
        #m_tree = generate_decision_tree(data[4000:8000],labels.copy())
        right = 0
        wrong = 0
        for item in data[step[i]:step[i+1]]:
        #for item in data[0:4000]:
            re = classify(m_tree,labels,item)
            if re == item['class']:
                right += 1
            else:
                wrong += 1
        print "right:"+str(right)+";wrong:"+str(wrong)
        total_right += right
    end = time.clock()
    print "build 10 model:read:%.2f s"% build_total
    print "all:read:%.2f s"% (end - start)
    print("total right:{0},total count:{1};rate:{2}").format(total_right,n,float(total_right)/n)
    #print step
    return total_right
