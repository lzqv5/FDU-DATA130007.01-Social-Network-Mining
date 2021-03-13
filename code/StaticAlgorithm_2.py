'''
Implementation of cluster_degree_dist method to found the seed nodes of graph maximizing influence
Coded by YOU, LUO
'''

from queue import PriorityQueue as PQ # priority queue
import networkx as nx
import  time

def CLD(G, k):
    '''
    Use the cluster and degree of node to measure influence,don't care the distance between the seed nodes
    :param G: networkx graph object
    :param k: the size of seed
    :return: S:seed nodes
    '''
    start_time = time.time()
    S = []
    CD = PQ()  #(1+cluster)*sum(degree of adjacent nodes)
    d = dict() #degree of each node
    for u in G.nodes():# 计算每个结点相应的出度
        d[u] = sum([G[u][v]['weight'] for v in G[u]])  # each edge adds degree 1
    for u in G.nodes():
        grade = -(1+nx.clustering(G,u))*sum([d[v] for v in G[u]])
        CD.put((grade,u))
    for i in range(k):
        if not CD.empty():
            grade,u = CD.get()
            S.append(u)
        else:
            break
    end_time = time.time()
    usetime = end_time - start_time
    return S , usetime

def CLD2(G, k):
    '''
    Use the cluster and degree of node to measure influence,don't care the distance between the seed nodes
    :param G: networkx graph object
    :param k: the size of seed
    :return: S:seed nodes
    '''
    start_time = time.time()
    S = []
    CD = PQ()  #(1+cluster)*degree of node
    grade = dict()
    for u in G.nodes():
        degree = sum([G[u][v]['weight'] for v in G[u]])  # each edge adds degree 1
        grade[u] = -(1+nx.clustering(G,u))*degree
        CD.put((grade[u],u))
    for i in range(k):
        if not CD.empty():
            grade,u = CD.get()
            S.append(u)
        else:
            break
    end_time = time.time()
    usetime = end_time - start_time
    return S , usetime



def CDD(G,k,d):
    '''
        Use the cluster and degree of node to measure influence, care the distance between the seed nodes
    :param G: networkx graph object
    :param k: the size of seed
    :param d: distance between seed nodes
    :return:
    '''
    start_time = time.time()
    S = []
    CD = PQ()  #(1+cluster)*sum(degree of adjacent nodes)
    degree = dict() #degree of each node
    for u in G.nodes():
        degree[u] = sum([G[u][v]['weight'] for v in G[u]])  # each edge adds degree 1
    for u in G.nodes():
        grade = -(1+nx.clustering(G,u))*sum([degree[v] for v in G[u]])
        CD.put((grade,u))
    grade, u = CD.get()
    S.append(u)
    if k >=2:
        count = 1
        while count<=k:
            if CD.empty():
                break
            grade,u = CD.get()
            distance = d
            for v in S :
                if(nx.has_path(G,source=v,target=u)) :
                    di = nx.has_path(G,source=v,target=u)
                    if di < d :
                        distance = di
                        break
            if distance < d:
                continue
            else:
                count += 1
                S.append(u)
    end_time = time.time()
    usetime = end_time - start_time
    return S , usetime


def CDD2(G,k,d):
    '''
        Use the cluster and degree of node to measure influence, care the distance between the seed nodes
    :param G: networkx graph object
    :param k: the size of seed
    :param d: distance between seed nodes
    :return:
    '''
    start_time = time.time()
    S = []
    CD = PQ()  #(1+cluster)*degree of adjacent
    grade = dict() #degree of each node
    for u in G.nodes():
        degree = sum([G[u][v]['weight'] for v in G[u]])  # each edge adds degree 1
        grade[u] = -(1+nx.clustering(G,u))*degree
        CD.put((grade[u],u))
    grade, u = CD.get()
    S.append(u)
    if k >=2:
        count = 1
        while count<=k:
            if CD.empty():
                break
            grade,u = CD.get()
            distance = d
            for v in S :
                if(nx.has_path(G,source=v,target=u)) :
                    di = nx.has_path(G,source=v,target=u)
                    if di < d :
                        distance = di
                        break
            if distance < d:
                continue
            else:
                count += 1
                S.append(u)

    end_time = time.time()
    usetime = end_time - start_time
    return S , usetime


def CDD2_optimization(G,k,d):
    '''
        Use the cluster and degree of node to measure influence, care the distance between the seed nodes
    :param G: networkx graph object
    :param k: the size of seed
    :param d: distance between seed nodes
    :return:
    '''
    start_time = time.time()
    S = []
    CD = PQ()  #(1+cluster)*degree of adjacent
    grade = dict() #degree of each node

    candidates = []
    seeds = []
    for node in G.nodes:
        candidates.append(node)
    candidates.sort(key=lambda x: G.out_degree(x), reverse=True)

    n = min(len(candidates),10*k)
    # Cut off some nodes with small out-degrees
    for u in candidates[:n]:
        degree = sum([G[u][v]['weight'] for v in G[u]])  # each edge adds degree 1
        grade[u] = -(1+nx.clustering(G,u))*degree
        CD.put((grade[u],u))
    grade, u = CD.get()
    S.append(u)
    if k >=2:
        count = 1
        while count<=k:
            if CD.empty():
                break
            grade,u = CD.get()
            distance = d
            for v in S :
                if(nx.has_path(G,source=v,target=u)) :
                    di = nx.has_path(G,source=v,target=u)
                    if di < d :
                        distance = di
                        break
            if distance < d:
                continue
            else:
                count += 1
                S.append(u)

    end_time = time.time()
    usetime = end_time - start_time
    return S , usetime





