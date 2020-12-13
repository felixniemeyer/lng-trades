import sqlite3
import datetime
import math
import numpy
import scipy
import plotly

# local
import Utils

db_connection = sqlite3.connect('db.db')
db_cursor = db_connection.cursor()

Scatter = plotly.graph_objs.Scatter
fig = plotly.graph_objs.Figure()

def add_to_degree_volumes(neighbors, degree_volumes, n, normalization_factor, x_date_in_days, square_sigma):
    ys = []
    i = 0
    for neighbor in neighbors:
        s = neighbors[neighbor]
        ys.append(numpy.zeros(n, numpy.float64))
        for flow in s:
            ts = flow.date.timestamp() / (60 * 60 * 24)
            weights = normalization_factor * numpy.exp( - (x_date_in_days - ts) ** 2 / (2 * square_sigma) )
            ys[i] = ys[i] + (weights * flow.volume)
        i += 1
    i = 0
    while len(degree_volumes) < len(ys): 
        degree_volumes.append(numpy.zeros(n, numpy.float64))
    for degree_volume in reversed(numpy.sort(ys,axis=0)):
        degree_volumes[i] += degree_volume
        i += 1

for flow_direction in ["in", "out"]:
    query = open("./queries/all-"+flow_direction+"-flows-ordered-by-node.sql").read()
    # query += " LIMIT 10" # increase processing for debugging

    class Flow:
        def __init__(self, volume, date):
            self.volume = volume
            self.date = date
        def __repr__(self):
            return self.volume.__str__() + ", " + self.date.__str__()

    from_date = datetime.datetime(2020, 2, 1)
    to_date = datetime.datetime(2020, 6, 15)
    stepsize = datetime.timedelta(days=1)
    n = math.ceil( (to_date - from_date) / stepsize ) 

    x_dates = numpy.empty(n, 'datetime64[D]')
    x_date_in_days = numpy.empty(n, numpy.uint64)
    for i in range(n):
        dt = from_date + i * stepsize
        x_dates[i] = dt
        x_date_in_days[i] = dt.timestamp() / (60 * 60 * 24)
        
    sigma = Utils.fwhm2sigma(15) # width at half height
    square_sigma = sigma ** 2 
    normalization_factor = 1 / ( sigma * math.sqrt(2 * math.pi) )

    degree_volumes = []
    current_node = None
    for row in db_cursor.execute(query):
        node = row[0]
        if(node != current_node):
            if(current_node != None): 
                add_to_degree_volumes(neighbors, degree_volumes, n, normalization_factor, x_date_in_days, square_sigma)
            neighbors = {}
            current_node = node
            neighbor_count = 0
        try: 
            neighbor = row[1]
            volume = int(row[2])
            date = datetime.datetime.fromtimestamp(row[3])
            if not neighbor in neighbors:
                neighbors[neighbor] = []
                neighbor_count += 1
            neighbors[neighbor].append(Flow(volume, date))
        except Exception as e:
            print("warning: skipping row", row, "because", e) 
                
    if(current_node != None):
        add_to_degree_volumes(neighbors, degree_volumes, n, normalization_factor, x_date_in_days, square_sigma)
    
    i = 1
    for degree_volume in degree_volumes:
        cf = 3 / (i + 2)
        color_string = "rgb(0,{},{})".format(int(78 * cf) + 50, 50 + int(205 * cf))
        if flow_direction == "out": 
            color_string = "rgb({},{},0)".format(int(205 * cf) + 50, 0 + int(78 * cf))
        fig.add_trace(Scatter(
            x=x_dates, y=degree_volume if flow_direction == "in" else -degree_volume,
            mode='lines', 
            name=flow_direction + "#{}".format(i if i != 6 else "..."),
            showlegend=i<7,
            line=dict(width=0.5, color=color_string),
            stackgroup=flow_direction
        ))
        i += 1
            
plotly.io.renderers.default = "firefox"
    
fig.update_layout(
    title="Volume of degrees on in and out flows", 
    yaxis_title="inflow [cubic meters / day]"
)
fig.show()

db_cursor.close()
