"""
created at on Tue Apr 21
Coded by Zhang
"""

import networkx as nx
import matplotlib.pyplot as plt
import time


# 可能在最终版本中通过命令行传递文件

#graph.nodes 里面包含了图的所有结点编号(ID)
#而每个graph.nodes[i]包含了第i+1个结点的所有卫星数据

def lir_compute(graph): # 计算每个结点的LIR值
    for n in graph.nodes:
        graph.nodes[n]['LIR'] = 0 #将每个结点的LIR值初始化
        for i in graph.successors(n): # 相当于n号结点的出度邻居集合
            if graph.out_degree(i) > graph.out_degree(n):
                graph.nodes[n]['LIR'] = graph.nodes[n]['LIR'] + 1


def select(graph, k, ul):  # k is the size of set, ul is the maximum
    candidates = []
    for n in graph.nodes:
        if graph.nodes[n]['LIR'] <= ul:
            candidates.append(n)
    candidates.sort(key=lambda x: graph.out_degree(x), reverse=True)
    return candidates[:k]  # return the top-K result


# G = nx.read_gpickle(filename)
def lir_select(G,k,ul):
    start_time = time.time()
    lir_compute(G)
    res = select(G, k, ul)
    end_time = time.time()
    usetime = end_time - start_time
    return res, usetime


"""
plt.figure()
plt.subplot(111)
nx.draw(G)
plt.show()
plt.savefig("C:\\Users\\Little_Zhang\\Desktop\\soc-Epinions1.png")
"""

# the graph is too large to draw
