'''
temporal network data from the filename.txt
generate a list which contents all the snapshots of the temporal network
Coded by LUO
'''
import networkx as nx

# 输入的文本数据中有3列：起始节点，终止结点，交流的时间戳。
# 本函数返回一个长度为 nums 的有向图列表，选择中间的
# 列表中的每一个有向图均为整个动态图的一个快照。
# 列表中的每个有向图元素G，G.graph['start']和G.graph['end']分别为图G的起始和结束的时间戳。
# 每个snapshot都可以视为一张静态图。
def snapshots_get_txt(filename,nums,fmt='txt'):
    '''
    :param filename:  filename as it says so.
    :param nums: the number of snapshots we need.
    :param fmt: format
    :return: A list contents all the snapshots of the network.
    '''
    # read in graph
    startNodes = []
    endNodes = []
    timeStamp = []
    with open(filename,'r') as f:
        for line in f:
            try:
                u, v, time = map(int, line.split())
                startNodes.append(u)
                endNodes.append(v)
                timeStamp.append(time)
            except:
                continue
    print("lenght:",len(timeStamp))

    timeSpan = timeStamp[-1] - timeStamp[0] + 1 #Total time span of the whole network's evolution

    singleSpan = timeSpan//(nums-1)  # Time span evenly allocated to each snapshot

    index = 0
    n = len(startNodes) # total records we can get from the file
    snapshots = []
    endTime = timeStamp[0] -1
    for i in range(nums):
        G = nx.DiGraph()
        startTime = endTime + 1  # get the starting time of this TimeWindow.
        endTime = startTime + singleSpan - 1
        G.graph['start'] = startTime
        G.graph['end'] = endTime
        while index < n and timeStamp[index] <= endTime:
            u, v = startNodes[index], endNodes[index]
            index += 1
            try:
                G[u][v]['weight'] += 1
            except:
                G.add_edge(u, v, weight=1)

        snapshots.append(G)

    if(timeSpan % nums): #read the last snapshot.
        G = nx.DiGraph()
        try:
            startTime = endTime + 1 # get the starting time of this TimeWindow.
            endTime = startTime + singleSpan - 1
            G.graph['start'] = startTime
            G.graph['end'] = endTime
            while index < n:
                u, v = startNodes[index], endNodes[index]
                index += 1
                try:
                    G[u][v]['weight'] += 1
                except:
                    G.add_edge(u, v, weight=1)
        except:
            pass

        snapshots.append(G)

    return snapshots


