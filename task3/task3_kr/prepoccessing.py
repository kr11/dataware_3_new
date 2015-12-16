# coding:utf-8
__author__ = 'kangrong'
import datetime
import time

#预处理
#checkin数量小于user_min的user,checkin数量小于location_min的元素被过滤
def prepoccesing(file_name,user_min,location_min,num = -1):
    fitting_location = []
    f = open(file_name)
    out = open("result.txt",'w')
    # first:filter the less user ,and count amount of locations data
    line = f.readline()
    i = 0
    user_num = {}
    location_num = {}
    datas = []
    d = None
    m_format = "%Y-%m-%dT%H:%M:%SZ"
    while(line != ''):
        i+=1
        if i % 100000 == 0:
            print i
        # if num == i:
        #     break
        checkins = line.strip().split('\t')
        d = datetime.datetime.strptime(checkins[1],m_format)
        user = int(checkins[0])
        location = int(checkins[4])
        tuple = (user,int(time.mktime(d.timetuple())),checkins[2],checkins[3],location)
        datas.append(tuple)
        if user_num.has_key(user) is False:
            user_num[user] = 1
        else:
            user_num[user] += 1
        if location_num.has_key(location) is False:
            location_num[location] = 1
        else:
            location_num[location] += 1
        line = f.readline()

    for item in datas:
        if user_num[item[0]] >= user_min and location_num[item[4]] >= location_min:
            out.write(str(item[0])+"\t"+str(item[1])+"\t"+item[2]+"\t"+item[3]+"\t"+str(item[4])+"\n")
    out.close()
    f.close()

def filter_friends(user_file,checkins_file):
    checkins_f = open(checkins_file)
    line = checkins_f.readline()
    i = 0

    fitting_users = set()
    while(line != ''):
        i+=1
        # if i % 100000 == 0:
        #     print i
        checkin = line.strip().split('\t')
        fitting_users.add(checkin[0])
        line = checkins_f.readline()
    checkins_f.close()

    user_f = open(user_file)
    line = user_f.readline()
    out = open('filter_edges.txt','w')
    while(line != ''):
        user_pair = line.strip().split('\t')
        if user_pair[0] in fitting_users and user_pair[1] in fitting_users:
            out.write(line)
        line = user_f.readline()
    out.close()

#prepoccesing("checkins.txt",50,100)
filter_friends("edges.txt","result.txt")