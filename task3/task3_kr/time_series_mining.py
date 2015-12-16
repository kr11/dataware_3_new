# coding:utf-8
__author__ = 'kangrong'

import matplotlib as mpl
import numpy as np
from matplotlib import pyplot as plt
from analyzing import *

# 绘制某个用户经过的经度/纬度的二维路线
def draw_path(user_id):
    #画一条曲线图
    #col_p = 0.1
    plt.figure(figsize=(8,8))   #设置图形的尺寸，单位为英尺
    long_lang = file_read_int("user_"+user_id+"_checkin.txt",[2,3])
    #print("target length:{0},actual length:{1}").format(1000,l)
    #l -= 1
    #print x
    #print y
    #x1 = np.arange(0,10,1)
    #lines = plt.plot(x,y)
    print len(long_lang[2])
    plt.plot(long_lang[2],long_lang[3],color='red',linewidth = 0.5)
    #plt.plot(x,y,'bo')
    plt.plot(long_lang[2],long_lang[3],'kp-.')
    plt.title('user_trace:'+user_id)
    #plt.ylabel('Function-Y')
    #plt.xlabel('Var-X')
    plt.legend()   #图形的右上角显示图形的标签，和上面的plt.plo(x,y,label='')有关
    #plt.setp(lines,color = 'r',linewidth = 2.5)

    plt.show()


# 绘制某个用户经过的经度/纬度
def statistic_steps(user_id,color):
    #画一条曲线图
    #col_p = 0.1
    long_lang = file_read_int("user_"+user_id+"_checkin.txt",[1,2,3])
    time_serires = np.array(long_lang[1])
    longtitude = np.array(long_lang[2])
    lantitude = np.array(long_lang[3])
    print len(long_lang[2])
    plt.figure(figsize=(12,4))   #设置图形的尺寸，单位为英尺
    plt.plot(time_serires,longtitude,color+'o',
             #time_serires,lantitude+np.average(longtitude)-np.average(lantitude),'k*'
             )

    #plt.plot(time_serires,'bo')
    #plt.plot(long_lang[2],long_lang[3],'kp-.')
    plt.title('user_trace:'+user_id)
    #plt.ylabel('Function-Y')
    #plt.xlabel('Var-X')
    plt.legend()   #图形的右上角显示图形的标签，和上面的plt.plo(x,y,label='')有关
    #plt.setp(lines,color = 'r',linewidth = 2.5)

    plt.show()


def get_location_cluster(dir):
    print "starting get cluster infomation"
    location_cluster = {}
    cluster_map = {}
    for i in range(47):
        cl = []
        f = open(dir+str(i)+'.txt')
        line = f.readline()
        while line != '':
            loc_id = int(line.strip())
            cl.append(loc_id)
            cluster_map[loc_id] = i
            line = f.readline()
        location_cluster[i] = cl
        f.close()
    print "starting get cluster infomation successfully"
    return location_cluster,cluster_map


# 输入n,s,一个用户user_id,一个时间点t,一个location聚类
# 根据前n个的预测t之后的s个点的预测情况比例
# 输出正确比例
def time_series_predict_cluster(n,s,user_id,t,location_cluster,cluster_map,user_data,checkin_data):
    right_count = 0
    times_temp = checkin_data[user_id]
    if n > len(times_temp) or t > len(times_temp):
        return None
    #过滤
    times = []
    for item in times_temp:
        if cluster_map.has_key(item[1]):
            times.append(item)
    #training
    #***************************
    #for i in range(n,t):
    #***************************
    if t+s > len(times):
        return -1
    best_type = cluster_map[times[t-n][1]]
    best_num = 1
    types = {best_type:1}
    # 添加前n个决策值
    for i in range(t-n+1,t):
        type = cluster_map[times[i][1]]
        if types.has_key(type) is False:
            types[type] = 1
        else:
            types[type] += 1
        if type == best_type:
            best_num += 1
        else:
            if types[type] > best_num:
                best_num = types[type]
                best_type = type
    # 开始预测
    if t+s > len(times):
        s = len(times)-t
    if s == 0:
        return -1
    for i in range(t,t+s-1):
        # 添加第i个值
        type = cluster_map[times[i][1]]
        if types.has_key(type) is False:
            types[type] = 1
        else:
            types[type] += 1
        # 删除第i-n个值
        del_type = cluster_map[times[i-n][1]]
        types[del_type] += 1
        if del_type == best_type:
            best_num -= 1
        # 更新best
        if type == best_type:
            best_num += 1
        else:
            if types[type] > best_num:
                best_num = types[type]
                best_type = type
        # best_type即为预测
        # 检验
        if best_type == cluster_map[times[i+1][1]]:
            right_count += 1

    return float(right_count)/s


def update_matrix(state_matrix,best_point,best_cluster,now_tuple,next_tuple,cluster_map,weight):
    now_loc = now_tuple[1]
    next_loc = next_tuple[1]
    #更新转移矩阵
    if state_matrix.has_key(now_loc) is False:
        state_matrix[now_loc] = {next_loc:weight}
    elif state_matrix[now_loc].has_key(next_loc) is False:
        state_matrix[now_loc][next_loc] = weight
    else:
        state_matrix[now_loc][next_loc] += weight
    #更新单点最优统计
    if best_point.has_key(now_loc) is False:
        #{"best_loc","num"}
        best_point[now_loc] = [next_loc,weight]
    else:
        if best_point[now_loc][0] == next_loc:
            best_point[now_loc][1] += weight
        else:
            next_loc_num = state_matrix[now_loc][next_loc]
            if next_loc_num > best_point[now_loc][1]:
                best_point[now_loc][0] = next_loc
                best_point[now_loc][1] = next_loc_num
    #更新聚类最优统计
    now_loc_cluster = cluster_map[now_loc]
    if best_cluster.has_key(now_loc_cluster) is False:
        best_cluster[now_loc_cluster] = [next_loc,weight]
    else:
        if best_cluster[now_loc_cluster][0] == next_loc:
            best_cluster[now_loc_cluster][1] += weight
        else:
            next_loc_num = state_matrix[now_loc][next_loc]
            if next_loc_num > best_cluster[now_loc_cluster][1]:
                best_cluster[now_loc_cluster][0] = next_loc
                best_cluster[now_loc_cluster][1] = next_loc_num


# 更新一个用户的数据到最新
def update_user(times,start_i,cut_timestamp,state_matrix,best_point,best_cluster,now_tuple,cluster_map,weight):
    times_l = len(times)
    while start_i < times_l:
        next_tuple = times[start_i]
        if next_tuple[0] >= cut_timestamp:
            break
        update_matrix(state_matrix,best_point,best_cluster,now_tuple,next_tuple,cluster_map,weight)
        now_tuple = next_tuple
        start_i+=1
    return start_i


# 输入n,一个用户user_id,一个时间点t,一个location聚类
# 根据所有的好友转移概率分析+自己的转移概率分析,输出准确度；
def friend_transfer(s,user_id,t,location_cluster,cluster_map,user_data,checkin_data,
                    geo_data,avg_cluster_dis,cluster_min_dis,geo_diagonal,self_weight=2):
    #print "calc friend_trnasfer:\t"+str(user_id)
    # 对于小于timestamp的数据,均认为是已知的.
    # 将user_id的所有好友行进轨迹添加到转移矩阵中,选择最大的.
    # 通过调节weight观察准确率
    self_times = checkin_data[user_id]
    if t >= len(self_times) or len(self_times) == 0:
        return [],[],[]
    if t+s > len(self_times):
        s = len(self_times)-t

    cut_timestamp = self_times[t][0]
    diff_rate_with_avg = []
    diff_rate_with_max = []
    diff_rate_with_min = []
    all_with_me = [user_id]
    for u in user_data[user_id]:
        #有数据的才进行计算
        if len(checkin_data[u]) > 0:
            all_with_me.append(u)
    state_matrix = {}
    best_point = {}
    best_cluster = {}
    all_user_i = {}
    right_count = 0
    #print "cut_time_stamp"+str(cut_timestamp)
    #预处理
    for u in all_with_me:
        times = checkin_data[u]
        weight = self_weight if u == user_id else 1
        #tuple:(time,location)
        all_user_i[u] = 1
        # 基于t之前的数据生成
        #print all_user_i
        #print u
        #print times[0:10]
        all_user_i[u] = update_user(times,all_user_i[u],cut_timestamp,state_matrix,best_point,best_cluster,times[all_user_i[u]-1],cluster_map,weight)

    # 对t之后的s各数据进行预测,并同时更新三个转移矩阵
    # 开始预测
    for i in range(t,t+s-1):
        cut_timestamp = self_times[i][0]
        for u in all_with_me:
            times = checkin_data[u]
            weight = self_weight if u == user_id else 1
            # 基于t之前的数据生成
            all_user_i[u] = update_user(times,all_user_i[u],cut_timestamp,state_matrix,best_point,best_cluster,times[all_user_i[u]-1],cluster_map,weight)

        # 预测
        self_now_loc = self_times[i][1]
        if best_point.has_key(self_now_loc) is True:
            predict_loc = best_point[self_now_loc][0]
        elif best_cluster.has_key(cluster_map[self_now_loc]) is True:
            predict_loc = best_cluster[cluster_map[self_now_loc]][0]
        else:
            predict_loc = self_times[i-1][1]
        # 检验,计算距离
        next_real_cluster = cluster_map[self_times[i][1]]
        predict_lola = geo_data[cluster_map[predict_loc]][predict_loc]
        real_lola = geo_data[next_real_cluster][self_times[i][1]]
        diff_dis = calc_distance_in_two_point(predict_lola[0],predict_lola[1],
                                              real_lola[0],real_lola[1])
        diff_rate_with_avg.append(diff_dis/avg_cluster_dis[next_real_cluster])
        diff_rate_with_min.append(diff_dis/cluster_min_dis[next_real_cluster])
        diff_rate_with_max.append(diff_dis/geo_diagonal[next_real_cluster])
        #精准预测的比例
        if predict_loc == self_times[i][1]:
            right_count+=1
        #print diff_dis,avg_cluster_dis[next_real_cluster],geo_diagonal[next_real_cluster]
    print("user_id:{0}\ttotal test:{1}\tright point:{2}\taccuracy rate\t:{3}").\
        format(user_id,s,right_count,float(right_count)/s)
    return diff_rate_with_avg,diff_rate_with_max,diff_rate_with_min


# 测试函数
def time_series_predict_cluster_hist():
    user_data = read_user('filter_edges.txt')
    checkin_data,geo_data,geo_diagonal = read_checkin_data('result.txt')
    location_cluster,cluster_map = get_location_cluster('location/')
    accuracy_stats = {}
    for i in range(3,10):
        accuracy_stats[i] = [0,0]
    for u in checkin_data:
        user_ts_len = len(checkin_data[u])
        predict_len = user_ts_len/2
        for i in range(3,10):

            if user_ts_len < predict_len +i:
                continue

            accuracy = time_series_predict_cluster(i,predict_len,u,user_ts_len-predict_len,location_cluster,cluster_map,user_data,checkin_data)
            if(accuracy != -1):
                accuracy_stats[i][0]+=accuracy
                accuracy_stats[i][1]+=1
                #print i,accuracy
                #print("forward n:{0},accuracy:{1}").format(i,)
    plt.figure(figsize=(8,4))

    ret = []
    for i in range(3,10):
        ret.append(float(accuracy_stats[i][0])/accuracy_stats[i][1])
    plt.plot(range(3,10),ret,'ro')
    plt.xlabel("forward n")
    plt.ylabel("accuracy rate")
    plt.title("time serires mining")
    plt.show()
    return 0
#draw_path("0")


def draw_diff_histogram(diff_rate_with_avg,diff_rate_with_max,diff_rate_with_min):
    fig, ax = plt.subplots(1,3,figsize=(30,8))
    ax[0].hist(diff_rate_with_avg,50)
    ax[0].set_title('compare with the average distance')
    ax[1].hist(diff_rate_with_max,50)
    ax[1].set_title('compare with the max distance')
    ax[2].hist(diff_rate_with_min,50)
    ax[2].set_title('compare with the min distance')
    plt.show()


def friend_transfer_hist():
    #准备
    cluster_num = 47
    location_cluster,cluster_map = get_location_cluster('location/')
    user_data = read_user('filter_edges.txt')
    checkin_data,geo_data,geo_diagonal = read_checkin_data('result.txt',cluster_map,cluster_num)
    cluster_avg_dis,cluster_min_dis = calc_avg_and_min_cluster_dis(geo_data,cluster_num)
    #对所有的
    predict_len = 50
    diff_rate_with_avg_sum=[]
    diff_rate_with_max_sum=[]
    diff_rate_with_min_sum=[]
    for u in checkin_data:
        user_ts_len = len(checkin_data[u])
        if user_ts_len < 2 * predict_len:
            predict_len = user_ts_len/2
        diff_rate_with_avg,diff_rate_with_max,diff_rate_with_min = \
            friend_transfer(predict_len,u,user_ts_len-predict_len,location_cluster,
                            cluster_map,user_data,checkin_data,geo_data,cluster_avg_dis,
                            cluster_min_dis,geo_diagonal,2)
        diff_rate_with_avg_sum += diff_rate_with_avg
        diff_rate_with_max_sum += diff_rate_with_max
        diff_rate_with_min_sum += diff_rate_with_min
        #print diff_rate_with_avg
        #print diff_rate_with_max

    draw_diff_histogram(diff_rate_with_avg_sum,diff_rate_with_max_sum,diff_rate_with_min_sum)




#time_series_predict_cluster_hist()
friend_transfer_hist()
