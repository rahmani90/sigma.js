import random
import pandas as pd
import hazm
import networkx as nx
import random
norm = hazm.Normalizer()
excel_file = 'data.xlsx'

df_edges = pd.read_excel(excel_file, sheet_name=0, header=0)
edges = df_edges.values.tolist()

df_nodes = pd.read_excel(excel_file, sheet_name=1, header=0)
df_nodes['cluster'] = df_nodes['cluster'].apply(str)
nodes = df_nodes.to_dict('records')


G=nx.from_pandas_edgelist(df_edges, 'source', 'destination')
pos = nx.fruchterman_reingold_layout(G)
#pos = nx.circular_layout(G)
#pos = nx.random_layout(G)
#pos = nx.spectral_layout(G)
#pos = nx.spring_layout(G)
for key, position in pos.items():
    for dic in nodes:
        if dic['key'] == key:
                dic['x']= list(position)[0]
                dic['y']= list(position)[1]
                dic['score']= G.degree()[key]
                

clusters_key=[]
clusters = ""
random.seed(2)
r = lambda: random.randint(0,255)
for i in zip(df_nodes['cluster'].values, df_nodes['tag'].values):
    if str(i[0]) not in clusters_key:
        random_color = '#%02X%02X%02X' % (r(),r(),r())
        clusters+= ", "+ str({"key": str(i[0]), "color": random_color, "clusterLabel": i[1]})
        clusters_key.append(str(i[0]))
clusters = clusters[1:]



json_str = """{
  "nodes": 
  """ + str(nodes) + """ ,
  "edges": """ + str(edges) + """  ,
  "clusters": [ """+clusters+""" ],
  "tags": [
    {"key": "مالی", "image": "charttype.svg" }
    
  ]
}"""

_ = open('dataset.json', 'w', encoding='utf-8').write(str(json_str).replace("'", '"'))
