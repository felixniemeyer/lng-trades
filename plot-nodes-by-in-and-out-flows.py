import matplotlib.pyplot as pyplot
import sqlite3

db_connection = sqlite3.connect('db.db')
db_cursor = db_connection.cursor()

node_names = []
node_inflows = []
node_outflows = []
for row in db_cursor.execute(open("./queries/in-and-out-flows.sql").read()):
	node_names.append(row[0])
	node_inflows.append(row[1])
	node_outflows.append(row[2])

db_cursor.close()
	
pyplot.ylabel('inflows')
pyplot.xlabel('outflows')
pyplot.scatter(x=node_outflows, y=node_inflows)

pyplot.savefig("./plots/in-and-out-flows.png", bbox_inches="tight")
pyplot.show()


