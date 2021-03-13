"""
Created at on Sun May 17
coded by LUO
"""

from copy import deepcopy
import networkx as nx
import time
import random
import numpy as np

# 度中心性
def DC_select(graph,k):
    '''
    :param graph: A directed graph.
    :param k: Size of the seed set.
    :return: Seed set.
    '''
    start_time = time.time()
    candidates = []
    for node in graph.nodes:
        candidates.append(node)
    # 按出度的大小降序排列
    candidates.sort(key=lambda x: graph.out_degree(x), reverse=True)
    end_time = time.time()
    use_time = end_time - start_time
    return candidates[:k],use_time

#随机选择
def Random_Select(graph,k):
    '''
    :param graph: A directed graph.
    :param k: Size of the seed set.
    :return: Seed set.
    '''
    start_time = time.time()
    candidates = []
    for node in graph.nodes:
        candidates.append(node)
    # 随机打乱
    random.shuffle(candidates)
    end_time = time.time()
    use_time = end_time - start_time
    return candidates[:k], use_time

#PageRank with Matrix iterative convergence.
def PageRank_select(graph,k,mode=0):
    '''
    :param graph: A directed graph.
    :param k: Size of the seed set.
    :param mode: type of return.
    :return: Seed set.
    '''
    if not mode in [0,1]:
        print("THE MODE IS NOT CORRECT!!")
        return None

    start_time = time.time()
    candidates = []
    for node in graph.nodes:
        candidates.append(node)

    # construct the adjacent matrix A
    A = []
    n = len(candidates)
    alpha = 0.85
    for node_i in candidates:
        row_i = []
        sum = 0
        for node_j in candidates:
            try:
                out = graph[node_i][node_j]['weight']
                row_i.append(alpha * out)
                sum += out
            except:
                row_i.append(0)

        if sum == 0:
            for i in range(n):
                row_i[i] = alpha / n
        else:
            for i in range(n):
                row_i[i] = row_i[i] / sum

        A.append(row_i)

    A = np.array(A)
    # 由于网络图模型中边的方向为影响力传播方向，而PageRank中边的方向
    # 为pagerank中心性的传播方向，二者相反，所以邻接矩阵A不作转置处理。
    # 效果等价于将网络图的边反向。
    # 所以这一步省略掉：A = A.T
    # term是A矩阵的纠正项
    term = np.ones((n, 1)) * ((1 - alpha) / n)
    A = A + term

    # We begin the iteration and compute the pagerank centrality.
    x = np.ones((n, 1)) / n
    x_next = np.matmul(A, x)
    diff = np.linalg.norm(x_next - x, ord=2)
    epsilon = 1e-3
    while diff >= epsilon:
        x = x_next
        x_next = np.matmul(A, x)
        diff = np.linalg.norm(x_next - x, ord=2)

    mapping = {}
    for i in range(n):
        mapping[candidates[i]] = x_next[i, 0]
    candidates.sort(key=lambda x: mapping[x], reverse=True)

    # finish the algorithm.
    end_time = time.time()
    use_time = end_time - start_time
    if mode == 0:
        return candidates[:k], use_time
    else:
        return candidates, use_time


# Some other algorithms to find the Top K nodes.
# Not used in the Final Version.
def similarity_compute(graph,candidate,seed):
    '''
    :param graph: A directed graph.
    :param candidate: node need to be checked.
    :param seed: node in seed set.
    :return: similarity between candidate and seed.
    '''

    set1 = set(graph.successors(candidate))
    set2 = set(graph.successors(seed))
    # norm = len(set1) + len(set2)
    norm = len(set1) + 1;
    # common = 2*len(set1.intersection(set2))
    common = len(set1.intersection(set2))
    return common / norm  # Dice coefficient
# Degree Centrality with Similarity Control-DCSC
def DCSC_select(graph,k,max_s):
    '''
    :param graph:  A directed graph.
    :param k: Size of seed set.
    :param max_s: Maximum similarity between the seeds.
    :return: Seed set.
    '''
    start = time.time()
    candidates = []
    seeds = []
    for node in graph.nodes:
        candidates.append(node)

    # 按出度的大小降序排列
    candidates.sort(key=lambda x: graph.out_degree(x), reverse=True)

    seeds.append(candidates[0])

    length = len(candidates)
    index_cur = 1 # the index of the candidate which is being checked.
    num = 1
    while num <=k : # Search for the rest k-1 seeds
        if index_cur >= length:
            break
        while index_cur < length:
            flag = 1
            for seed in seeds:
                sim = similarity_compute(graph,candidates[index_cur],seed)
                if sim > max_s:
                    flag = 0
                    break
            if flag == 1: # the candidate meet our requirement on similarity.
                break

            index_cur += 1

        #Every time the while loop breaks, one candidate can be appended to seeds
        seeds.append(candidates[index_cur])
        index_cur += 1
        num += 1
    end = time.time()
    use_time = end - start
    return seeds,use_time
def DCDC_select(graph,k,min_l):
    '''
    :param graph: A directed graph.
    :param k: Size of seed set.
    :param min_l: minimum distance between the seeds.
    :return: Seed set.
    '''
    start = time.time()
    candidates = []
    seeds = []
    for node in graph.nodes:
        candidates.append(node)

    # 按出度的大小降序排列
    candidates.sort(key=lambda x: graph.out_degree(x), reverse=True)

    seeds.append(candidates[0])

    length = len(candidates)
    index_cur = 1 # the index of the candidate which is being checked.
    num = 1
    while num <= k: # Search for the rest k-1 seeds
        if index_cur >= length:
            break
        while index_cur < length:
            flag = 1
            for seed in seeds:
                if(nx.has_path(graph,seed,candidates[index_cur])):
                    distance = nx.dijkstra_path_length(graph,seed,candidates[index_cur],weight='weight')
                else:
                    distance = min_l + 1

                if distance < min_l:
                    flag = 0
                    break
            if flag == 1: # the candidate meet our requirement on similarity.
                break

            index_cur += 1

        #Every time the while loop breaks, one candidate can be appended to seeds
        seeds.append(candidates[index_cur])
        index_cur += 1
        num += 1
    end = time.time()
    use_time = end - start
    return seeds , use_time