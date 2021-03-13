"""
File for Linear Threshold model (LT).
For directed graph G = (nodes, edges, weights) and
set of thresholds lambda for each node, LT model works as follows:
Initially set S of nodes is activated. For all outgoing neighbors,
we compare sum of edge weights from activated nodes and node thresholds.
If threshold becomes less than sum of edge weights for any given vertex,
then this vertex becomes active for the following iterations.
LT stops when no activation happens.

More on this: Kempe et al."Maximizing the spread of influence in a social network"
"""
"""
In Our initial model, set weights = 1
Modified by Zhang
"""

import random
from copy import deepcopy
import networkx as nx

# Ew -edge weight，即每一条边的权重
# Ew本身是一个字典，给定一个元组(v1,v2)即一条边，返回该边对应的权重。
def uniformWeights(G):
    """
    Every incoming edge of v with degree dv has weight 1/dv.
    """
    Ew = dict()
    for u in G:
        in_edges = G.in_edges([u], data=True)   # 返回给in_edges一个列表，列表里的每个元素都是一个元组(v1,v2)，
        dv = G.in_degree(u)#结点u的入度，记为dv   # 该列表存储的结点u的入边；
        for v1, v2, _ in in_edges:
            Ew[(v1, v2)] = 1 / dv
    return Ew


def randomWeights(G):
    """
    Every edge has random weight.
    After weights assigned,
    we normalize weights of all incoming edges so that they sum to 1.
    """
    Ew = dict()
    for u in G:
        in_edges = G.in_edges([u], data=True)
        ew = [random.random() for e in in_edges]  # random edge weights
        total = 0  # total sum of weights of incoming edges (for normalization)
        for num, (v1, v2, edata) in enumerate(in_edges):
            total += 1 * ew[num]
        for num, (v1, v2, _) in enumerate(in_edges):
            Ew[(v1, v2)] = ew[num] / total
    return Ew


def checkLT(G, Ew, eps=1e-4):
    ''' To verify that sum of all incoming weights <= 1
    '''
    for u in G:
        in_edges = G.in_edges([u], data=True)
        total = 0
        for (v1, v2, edata) in in_edges:
            total += Ew[(v1, v2)] * G[v1][v2]['weight']
        if total >= 1 + eps:
            return 'For node %s LT property is incorrect. Sum equals to %s' % (u, total)
    return True


def runLT(G, S, Ew):
    assert type(G) == nx.DiGraph, 'Graph G should be an instance of networkx.DiGraph'
    assert type(S) == list, 'Seed set S should be an instance of list'
    assert type(Ew) == dict, 'Influence edge weights Ew should be an instance of dict'
    """
        Input: G -- networkx directed graph
        S -- initial seed set of nodes
        Ew -- influence weights of edges
        NOTE: multiple k edges between nodes (u,v) are
        considered as one node with weight k. For this reason
        when u is activated the total weight of (u,v) = Ew[(u,v)]*k
        """
    T = deepcopy(S)  # targeted set
    lv = dict()  # threshold for nodes
    for u in G:
        lv[u] = random.random()

    W = dict(zip(G.nodes(), [0] * len(G)))  # weighted number of activated in-neighbors
    Sj = deepcopy(S)
    # print 'Initial set', Sj
    while len(Sj):  # while we have newly activated nodes
        Snew = []
        for u in Sj:
            try:
                for v in G[u]:
                    if v not in T:
                        W[v] += Ew[(u, v)] * 1  # G[u][v]['weight']
                        if W[v] >= lv[v]:
                            # print 'Node %s is targeted' %v
                            Snew.append(v)
                            T.append(v)
            except:
                continue
        Sj = deepcopy(Snew)
    return T


def avgLT(G, S, Ew, iterations):
    avgSize = 0
    progress = 1
    for i in range(iterations):
        if i == round(iterations * .1 * progress) - 1:
            progress += 1
        T = runLT(G, S, Ew)
        avgSize += len(T) / iterations

    return avgSize


"""
The following functions simulate the spread of influence on a dynamic network
coded by Zhang
"""


def Ksubgraph(G, S, k):
    """
        Input: G -- networkx directed graph
        S -- initial seed set of nodes
        k -- the step length
        :return k-step subgraph based on seeds S
        """
    nbunch = list()
    for n in S:
        if n in G.nodes:
            k_neighbour = nx.single_source_shortest_path_length(G, n, cutoff=k)  # 返回k阶以内的单源最短路
            neighbour_list = list(k_neighbour.keys())
            nbunch.extend(neighbour_list)
    nbunch = list(set(nbunch))  # 去重
    subG = G.subgraph(nbunch)
    return subG

def cleaner(G, S):
    """

    :param G: new graph
    :param S: seed
    :return: seed set without those seed not in G
    """
    for n in S:
        if n not in G.nodes:
            S.remove(n)
    return S

def run_LT_dynamic(snapshots, S, distance, iterations, random=True):
    """
    :param snapshots: a list of graphs
    :param S: seed set of nodes
    :param iteration: iteration times
    :param k: the length on each snapshot
    :param random: if random is TRUE, EW will be random; uniform other wise
    :return: a list of active nodes in different times on avg
    """

    k = len(snapshots)
    res = list()
    avgres = 0
    # print("length of snapshots:",k)

    for i in range(iterations):
        seed = S[:] # 特别注意的是，python中的列表赋值是浅拷贝，
                    # 所以此处需要将S的切片赋值给seed，以实现深拷贝。
        influenced = seed[:] # 切片赋值，理由同上，考虑浅拷贝因素。

        for j in range(k):
            G = snapshots[j]
            seed = cleaner(G, seed)
            subG = Ksubgraph(G, seed, distance)
            if random:
                Ew = randomWeights(subG)
            else:
                Ew = uniformWeights(subG)

            seed = runLT(subG, seed, Ew)
            influenced = influenced + seed

        avgres = avgres + len(list(set(influenced)))/iterations
    return avgres