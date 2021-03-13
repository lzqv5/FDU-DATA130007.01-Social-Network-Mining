"""
dynamic test
Coded by Zhang
"""
import networkx as nx
import random
import time
from queue import PriorityQueue as PQ  # priority queue
import matplotlib.pyplot as plt

from LIR import *
from Graph_get import *
from StaticAlgorithm_1 import *
from StaticAlgorithm_2 import *
from LT import *
from CDD_dynamic import *
from CDD2_dynamic import *
from DC_dynamic import *
from Graph_Snapshots import *


#filename = "dynamicdata//CollegeMsg-1.txt
filename ='ordered_digg.txt'
nums = 10 # length of TSN
history = 5 # Past
future = 5 # Future
G_snapshots = snapshots_get_txt(filename, nums)  # get networkx graph object
G_snapshots_his = G_snapshots[:history]
G_snapshots_fu = G_snapshots[history:]
iterations = 1000 # # of trials
distance = 3 # distance controlling
RANGE = 5  # propagation range in each snapshot
for i in range(nums):
    print('nodes:',G_snapshots[i].nodes)
    print('starTime:',G_snapshots[i].graph['start'])
    print('endTime:', G_snapshots[i].graph['end'])
    print("Node Size of the Snapshot:",len(G_snapshots[i].nodes))
    print("Edge Size of the Snapshot:", len(G_snapshots[i].edges))
    # pathlengths = [] #Compute the mean shortest path length of the Graph
    # for v in G_snapshots[i].nodes():
    #     spl = nx.single_source_shortest_path_length(G_snapshots[i], v)
    #     #print('%s %s' % (v, spl))
    #     for p in spl.values():
    #         pathlengths.append(p)
    # if len(pathlengths):
    #     print("average shortest path length:", (sum(pathlengths) / len(pathlengths)))
    # clustering = []  # Compute the mean clustering coefficient
    # for v in G_snapshots[i].nodes():
    #     clustering.append(nx.clustering(G_snapshots[i],v))
    # if len(clustering):
    #     print("average clustering coefficient :", (sum(clustering) / len(clustering)))

seed = dict()
usetime = dict()
influ = dict()

influ['CDD_linear'] = []
influ['CDD_hyp'] = []
influ['CDD_exp'] = []
influ['CDD2_linear'] = []
influ['CDD2_hyp'] = []
influ['CDD2_exp'] = []
influ['DC_linear'] = []
influ['DC_hyp'] = []
influ['DC_exp'] = []

seed_size = [i for i in range(1,11)]
for i in range(10):
    seed_size[i] = 10*seed_size[i]
for i in range(10):
    k = seed_size[i]
    print("k=", k)
    seed['CDD_linear'], usetime['CDD_linear'] = cdd_dynamic_linear(G_snapshots_his, k=k, num=history, min_distance=1)
    print("CDD_linear所用时间为", usetime['CDD_linear'])
    print("number:",len( seed['CDD_linear']),end=' ')
    print("CDD_linear:",seed['CDD_linear'])
    seed['CDD_hyp'], usetime['CDD_hyp'] = cdd_dynamic_hyp(G_snapshots_his, k=k, num=history, min_distance=1)
    print("CDD_hyp所用时间为", usetime['CDD_hyp'])
    print("number:", len(seed['CDD_hyp']), end=' ')
    print("CDD_hyp:", seed['CDD_hyp'])
    seed['CDD_exp'], usetime['CDD_exp'] = cdd_dynamic_exp(G_snapshots_his, k=k, num=history, min_distance=1)
    print("CDD_exp所用时间为", usetime['CDD_exp'])
    print("number:", len(seed['CDD_exp']), end=' ')
    print("CDD_exp:", seed['CDD_exp'])
    seed['CDD2_linear'], usetime['CDD2_linear'] = cdd2_dynamic_linear(G_snapshots_his, k=k, num=history, min_distance=distance)
    print("CDD2_linear所用时间为", usetime['CDD2_linear'])
    print("number:", len(seed['CDD2_linear']), end=' ')
    print("CDD2_linear:", seed['CDD2_linear'])
    seed['CDD2_hyp'], usetime['CDD2_hyp'] = cdd2_dynamic_hyp(G_snapshots_his, k=k, num=history, min_distance=distance)
    print("CDD2_hyp所用时间为", usetime['CDD2_hyp'])
    print("number:", len(seed['CDD2_hyp']), end=' ')
    print("CDD2_hyp:", seed['CDD2_hyp'])
    seed['CDD2_exp'], usetime['CDD2_exp'] = cdd2_dynamic_exp(G_snapshots_his, k=k, num=history, min_distance=distance)
    print("CDD2_exp所用时间为", usetime['CDD2_exp'])
    print("number:", len(seed['CDD2_exp']), end=' ')
    print("CDD2_exp:", seed['CDD2_exp'])
    seed['DC_linear'], usetime['DC_linear'] = DC_dynamic_linear(G_snapshots_his, k=k, num=history, min_distance=1)
    print("DC_linear所用时间为", usetime['DC_linear'])
    print("number:", len(seed['DC_linear']), end=' ')
    print("DC_linear:", seed['DC_linear'])
    seed['DC_hyp'], usetime['DC_hyp'] = DC_dynamic_hyp(G_snapshots_his, k=k, num=history, min_distance=1)
    print("DC_hyp所用时间为", usetime['DC_hyp'])
    print("number:", len(seed['DC_hyp']), end=' ')
    print("DC_hyp:", seed['DC_hyp'])
    seed['DC_exp'], usetime['DC_exp'] = DC_dynamic_exp(G_snapshots_his, k=k, num=history, min_distance=1)
    print("DC_exp所用时间为", usetime['DC_exp'])
    print("number:", len(seed['DC_exp']), end=' ')
    print("DC_exp:", seed['DC_exp'])

    print("1")
    influ['CDD_linear'].append(run_LT_dynamic(G_snapshots_fu, seed['CDD_linear'], distance=RANGE, iterations=iterations, random=False))
    print("2")
    influ['CDD_hyp'].append(run_LT_dynamic(G_snapshots_fu, seed['CDD_hyp'], distance=RANGE, iterations=iterations, random=False))
    print("3")
    influ['CDD_exp'].append(run_LT_dynamic(G_snapshots_fu, seed['CDD_exp'], distance=RANGE, iterations=iterations, random=False))
    print("4")
    influ['CDD2_linear'].append(run_LT_dynamic(G_snapshots_fu, seed['CDD2_linear'], distance=RANGE, iterations=iterations, random=False))
    print("5")
    influ['CDD2_hyp'].append(run_LT_dynamic(G_snapshots_fu, seed['CDD2_hyp'], distance=RANGE, iterations=iterations, random=False))
    print("6")
    influ['CDD2_exp'].append(run_LT_dynamic(G_snapshots_fu, seed['CDD2_exp'], distance=RANGE, iterations=iterations, random=False))
    print("7")
    influ['DC_linear'].append(run_LT_dynamic(G_snapshots_fu, seed['DC_linear'], distance=RANGE, iterations=iterations, random=False))
    print("8")
    influ['DC_hyp'].append(run_LT_dynamic(G_snapshots_fu, seed['DC_hyp'], distance=RANGE, iterations=iterations, random=False))
    print("9")
    influ['DC_exp'].append(run_LT_dynamic(G_snapshots_fu, seed['DC_exp'], distance=RANGE, iterations=iterations, random=False))

    print(seed)

plt.xlabel("seed_size")
plt.ylabel("Influence")
plt.title("LT MODEL- sx-mathoverflow")
plt.plot(seed_size, influ['CDD_linear'],'--')
plt.plot(seed_size, influ['CDD_hyp'],'--')
plt.plot(seed_size, influ['CDD_exp'],'--')
plt.plot(seed_size, influ['CDD2_linear'])
plt.plot(seed_size, influ['CDD2_hyp'])
plt.plot(seed_size, influ['CDD2_exp'])
plt.plot(seed_size, influ['DC_linear'],'--')
plt.plot(seed_size, influ['DC_hyp'],'--')
plt.plot(seed_size, influ['DC_exp'],'--')
plt.legend(['CLD_linear', 'CLD_hyp', 'CLD_exp', 'CDD2_linear', 'CDD2_hyp', 'CDD2_exp', 'DC_linear', 'DC_hyp', 'DC_exp']
           ,loc = 'lower right')
plt.show()

