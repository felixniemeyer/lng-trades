import sqlite3
import networkx
import matplotlib.pyplot as plt
import random 

NODE_MIN_VOLUME = 0 # show only nodes with a volume higher than that
NODE_LABEL_THRESHOLD = 5000000

random.seed(5)

db_connection = sqlite3.connect('db.db')
db_cursor = db_connection.cursor()

graph = networkx.DiGraph()

nodepos = {}
nodelabels = {}
query = open("./queries/nodes.sql").read()
for row in db_cursor.execute(query):
    node = row[0]
    inflow = row[1]
    outflow = row[2]
    if inflow + outflow > NODE_MIN_VOLUME:
        graph.add_node(node, inflow=inflow, outflow=outflow)
        nodepos[node] = (inflow / (inflow + outflow), random.random())
        nodelabels[node] = "" if inflow + outflow < NODE_LABEL_THRESHOLD else node.replace(" / ", "\n")

nodes = graph.nodes()
query = open("./queries/edges.sql").read()
for row in db_cursor.execute(query):
    origin = row[0]
    destination = row[1]
    if origin in nodes and destination in nodes:
        volume = row[2]
        deliveries = row[3]
        graph.add_edge(origin, destination, volume=int(volume), deliveries=int(deliveries))
    
weights = [graph[u][v]['volume'] * 0.000001 for u,v in graph.edges()]
sizes = [(graph.nodes[n]['inflow'] + graph.nodes[n]['outflow']) / 50000 for n in graph.nodes]
    
fig = plt.figure()
ax = fig.add_subplot()
networkx.draw_networkx(graph, node_color='#6688cc', edge_color=(0.9,0.8,0.4), pos=nodepos, width=weights, labels=nodelabels, ax=ax, node_size=sizes)
plt.tick_params(bottom=True, labelbottom=True)
plt.xlabel("inflow / total flow")
plt.title("Network")
plt.show()
plt.savefig("./results/network.png")

degrees = [graph.degree(n) for n in graph.nodes()]
plt.hist(degrees)
plt.title("Degree Distribution")
plt.xlabel("degree")
plt.ylabel("occurrences")
plt.show()

# plt.title("Weight-Degree Distribution")