import networkx as nx
import time
from queue import PriorityQueue as PQ # priority queue
import matplotlib.pyplot as plt
from LIR import *
from Graph_get import *
from DCSC import *
from cluster_degree_dist import *
from LT import *


filename = "CoraCitation.txt"
G = graph_get_txt(filename) #get networkx graph object
iterations = 1000
Ew = randomWeights(G)

seed_size = 100

distances = list(range(1,10))
influ = []

for distance in distances:
    print("distance=",distance)

    start = time.time()
    seed, usetime = CDD2(G, seed_size, d=distance)
    influ.append(avgLT(G, seed, Ew, iterations))
    print("Time Consuming :", time.time() - start)

plt.xlabel("Threshold of Distance")
plt.ylabel("Influence")
plt.title("LT MODE - CoraCitation")
plt.plot(distances,influ)
plt.show()