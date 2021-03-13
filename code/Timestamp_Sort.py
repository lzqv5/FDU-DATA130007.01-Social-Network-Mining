'''
Data preprocessing.
This py file is used to process the data to make the TimeStamp ordered.
coded by LUO.
'''

# Data Processing.
# run before the snapshots_get_txt(filename).
# Make the TimeStamps in order.
def TimeStamp_reorder(filename,fmt='txt'):
    '''
    :param filename: name of the file
    :param fmt: format
    :return: None
    '''
    # read in graph
    records = []
    with open(filename, 'r') as f:
        for line in f:
            try:
                u, v, timeStamp = map(int, line.split())
                records.append((u,v,timeStamp))
            except:
                continue
    records.sort(key=lambda x: x[2], reverse=False)
    n = len(records)
    rename  = 'ordered_'+filename
    with open(rename,'w') as out_file:
        for i in range(n):
            u, v, timeStamp = str(records[i][0]), str(records[i][1]), str(records[i][2])
            out_file.write(u +' '+ v +' '+timeStamp + '\n')
