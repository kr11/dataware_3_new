# coding:utf-8
__author__ = 'kangrong'
import generate_test_data

global test_data,labels

def init_labels():
    labels = {
        "age":False,
        "job":True,
        "marital":True,
        "education":True,
        "default":True,
        "housing":True,
        "loan":True,
        "contact":True,
        "month":True,
        "day_of_week":True,
        "duration":False,
        "campaign":False,
        "pdays":False,
        "previous":False,
        "poutcome":True,
        "emp.var.rate":False,
        "cons.price.idx":False,
        "cons.conf.idx":False,
        "euribor3m":False,
        "nr.employed":False,
        #'class':True
    }
    return labels


#读取csv文件返回
def read_file(file_name,labels):
    data = []
    l_len = len(labels)+1
    f = open(file_name)
    sp_title = f.readline().strip().replace('"','').split(';')
    sp_title[-1] = 'class'

    line = f.readline().strip()
    #s = 40000
    while line != '':
        # if s == 0:
        #     break
        # s -= 1
        sp = line.split(';')
        # if len(sp) != l_len:
        #     print line
        #     print 'error'
        #     break
        item = {}
        for i in range(0,len(sp_title)):
            if labels.has_key(sp_title[i]) is False or labels[sp_title[i]]:
                item[sp_title[i]] = sp[i]
            else:
                item[sp_title[i]] = float(sp[i])
        data.append(item)
        line = f.readline().strip()
    return data


#对处理的数据中的离散值属性，列出所有的可能取值
# get all value type for discrete labels
def get_all_value(result,data_set,labels):
    for lab in labels:
        if labels[lab]:
            if result.has_key(lab) is False:
                result[lab] = set()
            for item in data_set:
                result[lab].add(item[lab])
    return result
#read_file('1.csv',init_labels())
