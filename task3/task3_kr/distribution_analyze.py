# coding:utf-8
__author__ = 'kangrong'

from analyzing import *
import operator

import matplotlib.pyplot as plt
import numpy as np



#m = read_checkin('result.txt')
m = read_checkin('checkins.txt')
m_sorted = sorted(m.iteritems(), key=operator.itemgetter(1), reverse=True)
out = open("user_checkin_count.txt",'w')
for item in m_sorted:
    out.write(str(item[0])+"\t"+str(item[1])+"\n")

out.close()
vs = m.values()
vs.sort()
draw_friends(vs)
