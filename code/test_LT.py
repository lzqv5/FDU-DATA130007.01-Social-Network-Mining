'''
compare the influence between different algorithms
'''
import networkx as nx
import time
from queue import PriorityQueue as PQ # priority queue
import matplotlib.pyplot as plt
from LIR import *
from Graph_get import *
from DCSC import *
from cluster_degree_dist import *
from LT import *
#LT-Figeys-influ-opt
#filename = "F:\大二下\社交网络挖掘\项目实践\算法\graphdata\epi.txt"
filename = "arXiv_hep-th.txt"
G = graph_get_txt(filename) #get networkx graph object
iterations = 1000
Ew = randomWeights(G)

time1 = []
time2 = []
time3 = []
time4 = []
time5 = []
time6 = []
#time7 = []

influ1 = []
influ2 = []
influ3 = []
influ4 = []
influ5 = []
influ6 = []
#influ7 = []

seed_size = [i for i in range(1,11)]
for i in range(10):
    seed_size[i] = 25*seed_size[i]

for i in range(10):
    k = seed_size[i]
    print("k=",k)

    start = time.time()
    seed1, usetime1 = DC_select(G, k)  # DC method
    influ1.append(avgLT(G, seed1, Ew, iterations))
    time1.append(usetime1)
    print("Time Consuming :", time.time() - start)

    start = time.time()
    seed2, usetime2 = lir_select(G, k, ul=0)
    influ2.append(avgLT(G, seed2, Ew, iterations))
    time2.append(usetime2)
    print("Time Consuming :", time.time() - start)

    start = time.time()
    seed3, usetime3 = CLD2(G, k)
    influ3.append(avgLT(G, seed3, Ew, iterations))
    time3.append(usetime3)
    print("Time Consuming :", time.time() - start)

    start = time.time()
    seed4, usetime4 = CDD2(G, k, 3)
    influ4.append(avgLT(G, seed4, Ew, iterations))
    time4.append(usetime4)
    print("Time Consuming :", time.time() - start)

    start = time.time()
    seed5, usetime5 = Random_Select(G, k)
    influ5.append(avgLT(G, seed5, Ew, iterations))
    time5.append(usetime5)
    print("Time Consuming :", time.time() - start)

    start = time.time()
    seed6, usetime6 = CDD2_optimization(G, k,d=3)
    influ6.append(avgLT(G, seed6, Ew, iterations))
    time6.append(usetime6)
    print("Time Consuming :", time.time() - start)

    # start = time.time()
    # seed7, usetime7 = PageRank_select(G, k)
    # influ7.append(avgLT(G, seed7, Ew, iterations))
    # time7.append(usetime7)
    # print("Time Consuming :", time.time() - start)

plt.xlabel("Seed_size")
plt.ylabel("Influence")
plt.title("LT MODLE- Figeys")
plt.plot(seed_size,influ1,'--')
plt.plot(seed_size,influ2,'--')
plt.plot(seed_size,influ3,'--')
plt.plot(seed_size,influ4)
plt.plot(seed_size,influ5,'--')
plt.plot(seed_size,influ6)
#plt.plot(seed_size,influ7,'--')
plt.legend(["DC","LIR","CLD","CDD","Random","CDD with optimization"],loc = 'upper left')
plt.show()

name_list = seed_size[:]
# time1,...,time6
x = list(range(len(name_list)))
total_width, n = 0.6, 6
width = total_width / n
plt.bar(x,time1,width=width,label='DC',fc='r')
for i in range(len(x)):
    x[i] += width
plt.bar(x,time2,width=width,label='LIR',fc='m')
for i in range(len(x)):
    x[i] += width
plt.bar(x,time3,width=width,label='CLD',tick_label=name_list,fc='b')
for i in range(len(x)):
    x[i] += width
plt.bar(x,time4,width=width,label='CDD',fc='c')
for i in range(len(x)):
    x[i] += width
plt.bar(x,time5,width=width,label='Random',fc='g')
for i in range(len(x)):
    x[i] += width
plt.bar(x,time6,width=width,label='CDD with optimization',fc='lightskyblue')
# for i in range(len(x)):
#    x[i] += width
# plt.bar(x,time7,width=width,label='PageRank',fc='yellow')

plt.xlabel("Seed_size")
plt.ylabel("Time Consuming")
plt.title("LT MODLE- arXiv_hep-th")
plt.legend()
plt.show()