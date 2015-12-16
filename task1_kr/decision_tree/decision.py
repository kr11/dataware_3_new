# coding:utf-8
#__author__ = 'kangrong'

import math
import operator
import sys
from preprocessing.generate_test_data import *
from preprocessing.preprocessing import *
from decision_node import *
import datetime
import time
from test.fold_cross_validfication import *
global test_data,labels

# 计算信息增益
# calculate Claude Shannon
def calc_shannon_info(data_set):
    class_count = {}
    for item in data_set:
        #item = data_set[i]
        cl = item['class']
        if cl not in class_count.keys():
            class_count[cl] = 0
        class_count[cl] += 1
    shannon_info = 0.0
    s = len(data_set)
    for k in class_count:
        pi = float(class_count[k])/s
        shannon_info -= pi * math.log(pi,2)
    return shannon_info

#分区按照所给的分裂点，提取出符合要求的部分
def split_sub_data_set(data_set, label, split_value, less=None):
    ret = []
    #indiscrete labels
    if less is not None:
        for item in data_set:
            if is_match_gl(item[label],split_value,less):
                ret.append(item)
    else:
        for item in data_set:
            if item[label] == split_value:
                ret.append(item)
    return ret

# 判断所给值value与分裂点sp是否满足关系
# 包括两种情况：value<sp 且less = True
# 或value>sp且less=False
def is_match_gl(value, sp, less):
    it_is_less = value - sp
    if (it_is_less < 0 and less is True) or \
                (it_is_less > 0 and less is False):
        return True
    else:
        return False

#获取分区中分类占大多数的类别
def get_majority(data_set):
    class_count = {}
    for item in data_set:
        #item = data_set[i]
        cl = item['class']
        if cl not in class_count.keys():
            class_count[cl] = 0
        class_count[cl] += 1
    sortedClassCount = sorted(class_count.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

#选择最好的分类属性
def choose_best_label(data_set,labels):
    total_data_len = len(data_set)
    best_label = ''
    best_info_gain = sys.float_info.max
    best_sp = []
    best_group = {}
    for label in labels:
        #discrete
        if labels[label]:
            # for it in data_set:
            #     if it.has_key(label) is not True:
            #         print it
            #         exit()

            value_list = [it[label] for it in data_set]
            value_set = set(value_list)
            group = {}
            info_d = 0.0
            for v in value_set:
                sub_data_set = split_sub_data_set(data_set,label,v)
                group[v] = sub_data_set
                info_d += float(len(sub_data_set))/total_data_len * calc_shannon_info(sub_data_set)
            if info_d < best_info_gain:
                best_label = label
                best_info_gain = info_d
                best_sp = value_set
                best_group = group
        #indiscrete
        else:
            labels_list = [it[label] for it in data_set]
            labels_list = list(set(labels_list))
            if len(labels_list) == 1:
                best_label = label
                best_sp = labels_list[0]
                best_group['less'] = data_set
                return best_label,best_sp,best_group
            labels_list.sort()
            for i in range(0,len(labels_list)-1):
                info_d = 0.0
                sp = (labels_list[i+1]+labels_list[i])/2
                greater_data_set = split_sub_data_set(data_set,label,sp,False)
                info_d += float(len(greater_data_set))/total_data_len * calc_shannon_info(greater_data_set)
                less_data_set = split_sub_data_set(data_set,label,sp,True)
                info_d += float(len(less_data_set))/total_data_len * calc_shannon_info(less_data_set)
                if info_d < best_info_gain:
                    best_label = label
                    best_info_gain = info_d
                    best_sp = sp
                    best_group['less'] = less_data_set
                    best_group['greater'] = greater_data_set
    if best_label == '':
        print 'error'
    return best_label,best_sp,best_group


# 生成决策树
def generate_decision_tree(data_set,labels,types = None):
    node = DecisionTreeNode()
    # line 4~5
    if len(labels) == 0:
        node.classify = get_majority(data_set)
        return node

    class_list = [it['class'] for it in data_set]
    # line 2~3
    if(class_list.count(class_list[0]) == len(class_list)):
        node.classify = class_list[0]
        return node

    best_label,best_sp,best_group = choose_best_label(data_set,labels)
    if labels[best_label]:
        #discrete
        del labels[best_label]
        node.label = best_label
        sptree = {}
        for value in best_group:
            #node.sub_tree
            sptree[value] = generate_decision_tree(best_group[value],labels.copy())
            #node.push_sub(value,)
            #node.sub_tree[value].sub_tree = {}
        node.sub_tree = sptree
    else:
        #indiscrete
        del labels[best_label]
        node.label = best_label
        node.split_value = best_sp
        sptree = {}
        sptree['less'] = generate_decision_tree(best_group['less'],labels.copy())
        if best_group.has_key('greater'):
            sptree['greater'] = generate_decision_tree(best_group['greater'],labels.copy())
        node.sub_tree = sptree
    return node

#验证
def classify(d_tree, labels, test_item):
    #d_tree = DecisionTreeNode()
    if d_tree.classify is not None:
        return d_tree.classify
    label = d_tree.label
    v = test_item[d_tree.label]
    if labels[label]:
        if d_tree.sub_tree.has_key(v) is False:
            return 'no'
        classLabel = classify(d_tree.sub_tree[v],labels,test_item)
    else:
        is_less = v <= d_tree.split_value
        if is_less:
            classLabel = classify(d_tree.sub_tree['less'],labels,test_item)
        else:
            if d_tree.sub_tree.has_key('greater') is False:
                return 'no'
            classLabel = classify(d_tree.sub_tree['greater'],labels,test_item)
    return classLabel

#test_data = read_file('test.csv',init_labels())

# m_tree = generate_decision_tree(test_data,labels.copy())
# sys.stdout = open('tree','w')
# m_tree.print_node('')

labels = init_labels()
data = read_file("../preprocessing/1.csv",init_labels())
print 'read all data'

# test_k_fold_cross_validation(data,labels,10,generate_decision_tree,classify)
test_del_multi_labels(labels,data,generate_decision_tree,classify,10)
#test_k_fold_cross_validation_packet(data,labels,10,generate_decision_tree,classify)
