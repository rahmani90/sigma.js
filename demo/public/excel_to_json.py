import random
import pandas as pd
import hazm
import networkx as nx
import random

norm = hazm.Normalizer()
excel_file = 'data.xlsx'

df_edges = pd.read_excel(excel_file, sheet_name=0, header=0)
for i in range(len(df_edges)):
    df_edges.iloc[i]['source'] = norm.normalize(df_edges.iloc[i]['source']).replace('\u200c', ' ').strip()
    df_edges.iloc[i]['destination'] = norm.normalize(df_edges.iloc[i]['destination']).replace('\u200c', ' ').strip()

edges = []#df_edges.values.tolist()
for item in df_edges.values.tolist():
    edges.append([norm.normalize(item[0]).replace('\u200c', ' ').strip(), norm.normalize(item[1]).replace('\u200c', ' ').strip()])


df_nodes = pd.read_excel(excel_file, sheet_name=1, header=0)
df_nodes['cluster'] = df_nodes['cluster'].apply(str)
nodes = df_nodes.to_dict('records')

for i in range(len(nodes)):
	nodes[i]['key'] = norm.normalize(nodes[i]['key']).replace('\u200c', ' ').strip()
	nodes[i]['label'] = norm.normalize(nodes[i]['label']).replace('\u200c', ' ').strip()
	nodes[i]['tag'] = norm.normalize(nodes[i]['tag']).replace('\u200c', ' ').strip()


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
                #print(key)
        elif 'ابزارها' in key and 'ابزارها' in dic['key']:
            #print('[', "'", key, "'", ",", "'", dic['key'],"'", "]")
            pass



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

tags = []
for dic in nodes:
    tags.append(dic['tag'])
tags = list(set(tags))

json_str = """{
  "nodes": 
  """ + str(nodes) + """ ,
  "edges": """ + str(edges) + """  ,
  "clusters": [ """+clusters+""" ],
  "tags": [
    {"key": "حسابداری و حسابرسی در بازار سرمایه اسلامی", "image": "hesabdari.svg" },
    {"key": "مدیریت ریسک در بازار سرمایه اسلامی", "image": "risk.svg" },
    {"key": "قوانین و مقررات در بازار سرمایه اسلامی", "image": "ghavanin.svg" },
    {"key": "سایر", "image": "sayer.svg" },
    {"key": "نهادهای مالی فعال در بازار سرمایه اسلامی", "image": "nahad.svg" }, 
    {"key": "بازارهای مالی اسلامی", "image": "bazar.svg" },
    {"key": "طبقه بندی بازار سرمایه اسلامی", "image": "tabaghebazar.svg" },
    {"key": "مبانی، اصول و مفاهیم بازار سرمایه اسلامی", "image": "mabani.svg" },
    {"key": "ابزارهای مالی اسلامی", "image": "abzar.svg" }
  ]}"""

_ = open('dataset.json', 'w', encoding='utf-8').write(str(json_str).replace("'", '"'))
