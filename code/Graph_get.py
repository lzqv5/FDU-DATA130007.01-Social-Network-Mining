'''
Get graph( networks object ) from filename.txt or filename.gpickle
coded by YOU
'''
import networkx as nx

def graph_get_txt (filename,fmt='txt'):
    # read in graph
    G = nx.DiGraph()
    with open( filename ,'r') as f:
        n, m = f.readline().split()
        for line in f:
            try:
                u, v = map(int, line.split())
                try:
                    G[u][v]['weight'] += 1
                except:
                    G.add_edge(u,v, weight=1)
            except:
                continue
            # G.add_edge(u, v, weight=1)
    print ('The node number of graph is: ',n,' ,the edge number of graph is: ',m)
    return G