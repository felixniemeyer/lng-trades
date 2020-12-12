import sqlite3
import networkx
import matplotlib.pyplot as plt
import random 

NODE_MIN_VOLUME = 0 # show only nodes with a volume higher than that

random.seed(1)

db_connection = sqlite3.connect('db.db')
db_cursor = db_connection.cursor()

graph = networkx.DiGraph()

nodepos = {}
query = open("./queries/nodes.sql").read()
for row in db_cursor.execute(query):
    node = row[0]
    inflow = row[1]
    outflow = row[2]
    if inflow + outflow > NODE_MIN_VOLUME 
        graph.add_node(node, inflow=inflow, outflow=outflow)
        nodepos[node] = (inflow / (inflow + outflow) * 4, random.random() * 4)

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
    
networkx.draw(graph, pos=nodepos, width=weights)
plt.show()