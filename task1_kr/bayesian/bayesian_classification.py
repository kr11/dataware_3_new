# coding:utf-8
#__author__ = 'kangrong'
# Example of Naive Bayes implemented from Scratch in Python
import csv
import random
import math
import sys

from preprocessing.generate_test_data import *
from preprocessing.preprocessing import *
import time
from test.fold_cross_validfication import *
global test_data,labels

stats = {}

#按照所给分区分类
def separateByClass(dataset):
    separated = {}
    for item in dataset:
        #vector = dataset[i]
        if item['class'] not in separated:
            separated[item['class']] = []
        separated[item['class']].append(item)
    return separated

#求均值
def mean(numbers):
    return sum(numbers)/float(len(numbers))

#求方差
def stdev(numbers):
    if len(numbers) == 1:
        return 0
    avg = mean(numbers)
    variance = sum([pow(x-avg,2) for x in numbers])/float(len(numbers)-1)
    return math.sqrt(variance)


#计算beyes概率的模型
#对于连续值属性，求出均值和方差
#对于离散值，计算各种取值占该分类总数的比例
def calc_bayesian_model(dataset,labels,label_value_types):
    class_result = {}
    class_stat = {}
    v_len = len(dataset)
    for label in labels:
        if labels[label]:
            #discrete
            value_count = {}
            for item in dataset:
                cl = item[label]
                if cl not in value_count.keys():
                    value_count[cl] = 0
                value_count[cl] += 1
            zero_num = 0
            for vt in label_value_types[label]:
                if value_count.has_key(vt) is False:
                    zero_num += 1
                    value_count[vt] = 1
            class_result[label] = {}
            class_stat[label] = {}
            for v in value_count:
                class_result[label][v] = float(value_count[v]) / (v_len+zero_num)
                class_stat[label][v] = value_count[v]
        else:
            #indiscrete
            attr_values = [item[label] for item in dataset]
            class_result[label] = (mean(attr_values), stdev(attr_values))
    return class_result,class_stat


# 得到bayes模型
def bayesian_exe_by_class(dataset,labels,label_value_types):
    separated = separateByClass(dataset)
    result = {}
    for classValue, instances in separated.iteritems():
        result[classValue],stats[classValue] = calc_bayesian_model(instances,labels,label_value_types)
    return result


# 计算连续值属性取x时该属性下的先验概率
def calculateProbability(x, mean, stdev):
    if stdev == 0:
        return 1
    exponent = math.exp(-(math.pow(x-mean,2)/(2*math.pow(stdev,2))))
    return (1 / (math.sqrt(2*math.pi) * stdev)) * exponent


# 计算所有属性的联合先验概率
# calculate all probablilities of each label
def calculate_class_probabilities(bayes_model, inputVector,labels):
    probabilities = {}
    for class_type, class_model in bayes_model.iteritems():
        probabilities[class_type] = 1
        for label,lab_model in class_model.iteritems():
            x_value = inputVector[label]
            if labels[label]:
                probabilities[class_type] *= lab_model[x_value]
            else:
                mean, stdev = lab_model
                probabilities[class_type] *= calculateProbability(x_value, mean, stdev)
    return probabilities


#验证
# given a trained summaries and an input
# using calculateClassProbabilities to calculate all probablilities of each label
# and choose the best label which means its prob is minimum
def predict(bayes_model,labels,item):
    probabilities = calculate_class_probabilities(bayes_model, item,labels)
    bestLabel, bestProb = None, -1
    for classValue, probability in probabilities.iteritems():
        if bestLabel is None or probability > bestProb:
            bestProb = probability
            bestLabel = classValue
    return bestLabel

#获取所有测试数据的判断
def getPredictions(bayes_model, testSet,labels):
    predictions = []
    for i in range(len(testSet)):
        result = predict(bayes_model, testSet[i],labels)
        predictions.append(result)
    return predictions

#测试任意一个属性删除后得到的结果
def test_del_labels(labels,data):
    temp = sys.stdout
    n = len(data)
    for label in labels:
        temp_labels = labels.copy()
        del temp_labels[label]
        print "del:"+label
        sys.stdout = open('del_'+label + '.csv','w')
        print "del:"+label
        total_right = test_k_fold_cross_validation_plus(data,temp_labels,10)
        sys.stdout.close()
        #draw_histogram(label,data)
        sys.stdout = temp
        print("total right:{0},total count:{1};rate:{2}").format(total_right,n,float(total_right)/n)


#绘制直方图
def test_del_labels_histogram(labels,data):
    for label in labels:
    #for label in ['pdays','euribor3m']:
        draw_histogram(label,data)

#直方图
def draw_histogram(label,data):
    print label
    n = len(data)
    histogram = {}
    temp = sys.stdout
    sys.stdout = open('histogram_'+label+'.csv','w')
    no_count = 0
    a = 1
    b = 1.1
    for item in data:
        if isinstance(item[label],int):
            l = int(item[label])
        elif isinstance(item[label],float):
            l = float(item[label])
        else:
            l = item[label]
        if histogram.has_key(l) is False:
            histogram[l] = [0,0,0]
        histogram[l][0] += 1
        if item['class'] == '"no"':
            histogram[l][1] += 1
            no_count += 1
        else:
            histogram[l][2] += 1
    histogram = sorted(histogram.items(), key=lambda d:d[0])
    for item in histogram:
        print str(item[0])+':',
        v = item[1]
        print("{0},{1},{2},{3}").format(v[0],v[1],v[2],round(float(v[2]*100)/v[0],4))
    #print("total:{0},{1},{2},{3}").format(n,no_count,n-no_count,round(float((n-no_count)*100)/n,4))
    sys.stdout.close()
    sys.stdout = temp


labels = init_labels()
data = read_file("../preprocessing/1.csv",init_labels())
# exit()

print 'read all data'
#test_k_fold_cross_validation(data,labels,10,bayesian_exe_by_class,predict)
test_k_fold_cross_validation_packet(data,labels,10,bayesian_exe_by_class,predict)
#test_del_multi_labels(labels,data,bayesian_exe_by_class,predict,10)
