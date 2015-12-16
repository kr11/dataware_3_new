# coding:utf-8
__author__ = 'kangrong'

import numpy as np
import math
import sys
import matplotlib.pyplot as plt
import random
#从Gowalla_edges中读文件,返回一个字典
def read_user(user_file,num = -1):
    user_relation = {}
    f = open(user_file)
    line = f.readline()
    i = 0
    while(line != ''):
        i+=1
        # if i % 100000 == 0:
        #     print i
        if num == i:
            break
        friends = line.strip().split('\t')
        start = int(friends[0])
        end = int(friends[1])
        if user_relation.has_key(start) is False:
            user_relation[start] = []
        user_relation[start].append(end)
        line = f.readline()

    return user_relation


# 从Gowalla_edges中读文件,返回一个字典,字典为每个用户的登录数
def read_checkin(checkin_file,num = -1):
    checkin= {}
    f = open(checkin_file)
    line = f.readline()
    i = 0
    while(line != ''):
        i+=1
        if i % 100000 == 0:
            print i
        if num == i:
            break
        friends = line.strip().split('\t')
        #user = friends[0]
        user = friends[4]
        if checkin.has_key(user) is False:
            checkin[user] = 1
        else:
            checkin[user] += 1
        line = f.readline()

    return checkin


# 读取checkin入一个字典:{user:[t1,t2,...]}
def read_checkin_data(checkin_file,cluster_map= None,cluster_num=0,num = -1):
    checkin = {}
    geo_data_by_cluster = []
    geo_area_by_cluster = []
    if cluster_map is not None:
        for i in range(cluster_num):
            geo_data_by_cluster.append({})
            # 边界:分别对应longitude_min, max, latitude_min, max
            geo_area_by_cluster.append([0,0,0,0])

    f = open(checkin_file)
    line = f.readline()
    i = 0
    while(line != ''):
        i+=1
        if i % 100000 == 0:
            print i
        if num == i:
            break
        item = line.strip().split('\t')
        #user = friends[0]
        user = int(item[0])
        loc = int(item[4])
        if checkin.has_key(user) is False:
            checkin[user] = []
        if cluster_map is not None:
            # 如果有cluster信息,就要过滤掉被删除的点
            if cluster_map.has_key(loc):
                checkin[user].append((int(item[1]),loc))
            else:
                line = f.readline()
                continue
        else:
            checkin[user].append((int(item[1]),loc))

        if cluster_map is not None:
            cluster_i = cluster_map[loc]
            if geo_data_by_cluster[cluster_i].has_key(loc) is False:
                lo = float(item[2])
                la = float(item[3])

                geo_data_by_cluster[cluster_i][loc] = (lo,la)
                # 确定边界
                if lo < geo_area_by_cluster[cluster_i][0]:
                    geo_area_by_cluster[cluster_i][0] = lo
                elif lo > geo_area_by_cluster[cluster_i][1]:
                    geo_area_by_cluster[cluster_i][1] = lo
                if la < geo_area_by_cluster[cluster_i][2]:
                    geo_area_by_cluster[cluster_i][2] = la
                elif la > geo_area_by_cluster[cluster_i][3]:
                    geo_area_by_cluster[cluster_i][3] = la


        line = f.readline()
    f.close()
    #计算对角线边界
    geo_diagonal = []
    if cluster_map is not None:
        for i in range(cluster_num):
            area = geo_area_by_cluster[i]
            geo_diagonal.append(calc_distance_in_two_point(area[0],area[2],area[1],area[3]))

    return checkin,geo_data_by_cluster,geo_diagonal


def calc_distance_in_two_point(long1,lang1,long2,lang2):
    return math.sqrt((long1-long2)**2+(lang1-lang2)**2)


def calc_avg_and_min_cluster_dis(geo_data,cluster_num):
    print "calc cluster sverage distance"
    cluster_avg_dis = []
    cluster_min_dis = []
    for i in range(cluster_num):
        #随机寻找100个点
        geo_i = geo_data[i]
        l = len(geo_i)
        n_list = geo_i.keys()
        cal_l = l if l < 100 else 100
        #选cal_l个点
        ran_result = random.sample(n_list,cal_l)
        ran_result.sort()
        dis_sum = 0.0
        min_dis = sys.float_info.max
        for s in ran_result:
            for j in ran_result:
                dis = calc_distance_in_two_point(geo_i[s][0],geo_i[s][1],geo_i[j][0],geo_i[j][1])
                dis_sum += dis
                if min_dis > dis and dis != 0:
                    min_dis = dis
        cluster_avg_dis.append(dis_sum/(cal_l*(cal_l-1)))
        cluster_min_dis.append(min_dis)
    print "calc cluster sverage distance successfully"
    return cluster_avg_dis,cluster_min_dis

def dist_count(friends):
    result = []
    for k,v in friends.iteritems():
        result.append(len(v))
    result.sort()
    return result

#input an array of integer
def draw_friends(count):
    #count = dist_count(count)
    plt.figure(figsize=(8,4))
    plt.xlabel("user")
    plt.ylabel("friends count")
    plt.title("checkin statistic")
    print max(count)
    #start_index = 1279000
    start_index = 0
    end_index =1000
    #plt.hist([1,2],50)
    #plt.hist(count)
    plt.plot(np.arange(start_index,len(count),1), count[start_index:])
    #plt.plot(np.arange(start_index,end_index,1), count[start_index:end_index])
    plt.show()


# 一个以"\t"分割的文件
# 输入一组序号,返回这些列
def file_read_int(file_name, columns, num = -1):
    result = {}
    for col in columns:
        result[col] = []

    f = open(file_name)
    line = f.readline()
    i = 0
    while(line != ''):
        i+=1
        # if i % 100000 == 0:
        #     print i
        if num == i:
            break
        items = line.strip().split('\t')
        for col in columns:
            result[col].append(float(items[col]))
        line = f.readline()

    return result




