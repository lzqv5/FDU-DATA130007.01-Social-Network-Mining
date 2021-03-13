'''
 use forget_remember mechanism and CDD method to find the seed
 Coded by YOU
'''

from queue import PriorityQueue as PQ # priority queue
import networkx as nx
import time
import numpy as np



def cdd_dynamic_linear(G_snapshots,k,num,min_distance):
    '''
    cdd method with linear forgetting : sum( l * grade(l)^l ),
    use (1+cluster)*sum(degree of adjacent nodes) to grade nodes
    :param G_snapshots: graph_snapshots list get from dynamic graph
    :param k:  seed size
    :param num: number of snapshots used to find seed
    :return: seed , usetime
    '''
    num = num - 1
    hist = []
    for i in range(num):
        grade_dict = dict()
        graph = G_snapshots[i]
        degree = dict()
        for u in graph.nodes():
            degree[u] = sum([graph[u][v]['weight'] for v in graph[u]])  # each edge adds degree 1
        degree_list = list(degree.values())
        degree_list.sort(reverse = True)
        degree_uselist = degree_list[0:20*k]
        nodes_use = {key for key, value in degree.items() if value in degree_uselist}
        for u in nodes_use:
            grade = -(1 + nx.clustering(graph, u)) * sum([degree[v] for v in graph[u]])
            grade_dict[u] = grade
        hist.append(grade_dict)
    #之前历史得分的计算时间不算入寻找当前seed所用的时间
    start_time = time.time()
    graph = G_snapshots[num]
    grade_dict = dict()
    degree = dict()
    for u in graph.nodes():
        degree[u] = sum([graph[u][v]['weight'] for v in graph[u]])  # each edge adds degree 1
    degree_list = list(degree.values())
    degree_list.sort(reverse=True)
    degree_uselist = degree_list[0:20 * k]
    nodes_use = {key for key, value in degree.items() if value in degree_uselist}
    for u in nodes_use:
        grade = -(1 + nx.clustering(graph, u)) * sum([degree[v] for v in graph[u]])
        grade_dict[u] = grade
    hist.append(grade_dict)

    candidates = grade_dict.keys()
    CD = PQ()
    S = []
    for u in candidates:
        grade = 0
        for i in range(num+1):
            Dict = hist[i]
            if len(Dict):
                Avg = sum(Dict.values())/len(Dict)
            else:
                Avg = 0
            if Dict.get(u) :
                grade -= (i+1)*(Dict[u]) ** (i+1)
            else :
                grade -= (i+1)*Avg ** (i+1)
        CD.put([grade,u])
    grade, u = CD.get()
    S.append(u)
    if k >=2:
        count = 1
        while count<=k:
            if CD.empty():
                break
            grade,u = CD.get()
            distance = min_distance
            for v in S :
                if(nx.has_path(graph,source=v,target=u)) :
                    di = nx.has_path(graph,source=v,target=u)
                    if di < min_distance:
                        distance = di
                        break
            if distance < min_distance:
                continue
            else:
                count += 1
                S.append(u)

    use_time = time.time() - start_time

    return S , use_time


def cdd_dynamic_hyp(G_snapshots, k, num, min_distance):
    '''
    cdd method with hyperbolic forgetting :sum( 1/(K-l+1) * grade(l)^l ),
    use (1+cluster)*sum(degree of adjacent nodes) to grade nodes
    :param G_snapshots: graph_snapshots list get from dynamic graph
    :param k:  seed size
    :param num: number of snapshots used to find seed
    :return: seed , usetime
    '''
    num = num - 1
    hist = []
    for i in range(num):
        grade_dict = dict()
        graph = G_snapshots[i]
        degree = dict()
        for u in graph.nodes():
            degree[u] = sum([graph[u][v]['weight'] for v in graph[u]])  # each edge adds degree 1
        degree_list = list(degree.values())
        degree_list.sort(reverse = True)
        degree_uselist = degree_list[0:20*k]
        nodes_use = {key for key, value in degree.items() if value in degree_uselist}
        for u in nodes_use:
            grade = -(1 + nx.clustering(graph, u)) * sum([degree[v] for v in graph[u]])
            grade_dict[u] = grade
        hist.append(grade_dict)
    #之前历史得分的计算时间不算入寻找当前seed所用的时间
    start_time = time.time()
    graph = G_snapshots[num]
    grade_dict = dict()
    degree = dict()
    for u in graph.nodes():
        degree[u] = sum([graph[u][v]['weight'] for v in graph[u]])  # each edge adds degree 1
    degree_list = list(degree.values())
    degree_list.sort(reverse=True)
    degree_uselist = degree_list[0:20 * k]
    nodes_use = {key for key, value in degree.items() if value in degree_uselist}
    for u in nodes_use:
        grade = -(1 + nx.clustering(graph, u)) * sum([degree[v] for v in graph[u]])
        grade_dict[u] = grade
    hist.append(grade_dict)

    candidates = grade_dict.keys()
    CD = PQ()
    S = []
    for u in candidates:
        grade = 0
        for i in range(num + 1):
            Dict = hist[i]
            if len(Dict):
                Avg = sum(Dict.values())/len(Dict)
            else:
                Avg = 0
            if Dict.get(u):
                grade -= 1/(num+1-i) * (Dict[u]) ** (i+1)
            else:
                grade -= 1/(num+1-i) * Avg ** (i+1)
        CD.put([grade, u])
    grade, u = CD.get()
    S.append(u)
    if k >= 2:
        count = 1
        while count <= k:
            if CD.empty():
                break
            grade, u = CD.get()
            distance = min_distance
            for v in S:
                if (nx.has_path(graph, source=v, target=u)):
                    di = nx.has_path(graph, source=v, target=u)
                    if di < min_distance:
                        distance = di
                        break
            if distance < min_distance:
                continue
            else:
                count += 1
                S.append(u)

    use_time = time.time() - start_time

    return S, use_time

def cdd_dynamic_exp(G_snapshots, k, num, min_distance):
    '''
    cdd method with exponential forgetting : sum(exp(l)*grade(l))
    use (1+cluster)*sum(degree of adjacent nodes) to grade nodes
    :param G_snapshots: graph_snapshots list get from dynamic graph
    :param k:  seed size
    :param num: number of snapshots used to find seed
    :return: seed , usetime
    '''
    num = num - 1
    hist = []

    for i in range(num):
        grade_dict = dict()
        degree = dict()
        graph = G_snapshots[i]
        for u in graph.nodes():
            degree[u] = sum([graph[u][v]['weight'] for v in graph[u]])  # each edge adds degree 1
        degree_list = list(degree.values())
        degree_list.sort(reverse = True)
        degree_uselist = degree_list[0:20*k]
        nodes_use = {key for key, value in degree.items() if value in degree_uselist}
        for u in nodes_use:
            grade = -(1 + nx.clustering(graph, u)) * sum([degree[v] for v in graph[u]])
            grade_dict[u] = grade
        hist.append(grade_dict)
    #之前历史得分的计算时间不算入寻找当前seed所用的时间
    start_time = time.time()
    graph = G_snapshots[num]
    grade_dict = dict()
    degree = dict()
    for u in graph.nodes():
        degree[u] = sum([graph[u][v]['weight'] for v in graph[u]])  # each edge adds degree 1
    degree_list = list(degree.values())
    degree_list.sort(reverse=True)
    degree_uselist = degree_list[0:20 * k]
    nodes_use = {key for key, value in degree.items() if value in degree_uselist}
    for u in nodes_use:
        grade = -(1 + nx.clustering(graph, u)) * sum([degree[v] for v in graph[u]])
        grade_dict[u] = grade
    hist.append(grade_dict)

    candidates = grade_dict.keys()
    CD = PQ()
    S = []
    for u in candidates:
        grade = 0
        for i in range(num + 1):
            Dict = hist[i]
            if len(Dict):
                Avg = sum(Dict.values())/len(Dict)
            else:
                Avg = 0
            if Dict.get(u):
                grade -= np.exp(i) * (Dict[u])** (i + 1)
            else:
                grade -= np.exp(i) * Avg** (i + 1)
        CD.put([grade, u])
    grade, u = CD.get()
    S.append(u)
    if k >= 2:
        count = 1
        while count <= k:
            if CD.empty():
                break
            grade, u = CD.get()
            distance = min_distance
            for v in S:
                if (nx.has_path(graph, source=v, target=u)):
                    di = nx.has_path(graph, source=v, target=u)
                    if di < min_distance:
                        distance = di
                        break
            if distance < min_distance:
                continue
            else:
                count += 1
                S.append(u)

    use_time = time.time() - start_time

    return S, use_time
