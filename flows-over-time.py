import sqlite3
import datetime
import math
import numpy
import scipy
import plotly
import colorhash
import optparse

# local
import Utils

op = optparse.OptionParser()
op.add_option("-z", "--zone", dest="zone", default="Dahej")
op.add_option("-i", "--installation", dest="installation", default="Dahej")
(options, args) = op.parse_args()

db_connection = sqlite3.connect('db.db')
db_cursor = db_connection.cursor()

Scatter = plotly.graph_objs.Scatter
fig = plotly.graph_objs.Figure()

for flow_direction in ["in", "out"]:
    query = open("./query-templates/"+flow_direction+"-flows-of-a-node.sql").read()
    query = query.replace('$zone', options.zone)
    query = query.replace('$installation', options.installation)

    class Flow:
        def __init__(self, volume, date):
            self.volume = volume
            self.date = date
        def __repr__(self):
            return self.volume.__str__() + ", " + self.date.__str__()

    neighbors = {}
    init_date_range = True
    for row in db_cursor.execute(query):
        try: 
            neighbor = row[0] + ' / ' + row[1]
            volume = int(row[2])
            date = Utils.parse_datetime(row[3])
            if not neighbor in neighbors:
                neighbors[neighbor] = []
            neighbors[neighbor].append(Flow(volume, date))
            
            if init_date_range: 
                init_date_range = False
                from_date = date
                to_date = date
            else:
                if date < from_date:
                    from_date = date
                if date > to_date:
                    to_date = date
        except Exception as e:
            print("warning: skipping row", row, "because", e) 
                
    from_date = datetime.datetime(2020, 2, 1)
    to_date = datetime.datetime(2020, 6, 15)
    stepsize = datetime.timedelta(days=1)
    datapoints = math.ceil( (to_date - from_date) / stepsize ) 

    x_dates = numpy.empty(datapoints, 'datetime64[D]')
    x_date_in_days = numpy.empty(datapoints, numpy.uint64)
    for i in range(datapoints):
        dt = from_date + i * stepsize
        x_dates[i] = dt
        x_date_in_days[i] = dt.timestamp() / (60 * 60 * 24)
        
    sigma = Utils.fwhm2sigma(20) # width at half height
    square_sigma = sigma ** 2 
    normalization_factor = 1 / ( sigma * math.sqrt(2 * math.pi) )

    y = {}
    sign = 1
    if flow_direction == "out": 
        sign = -1
    for neighbor in neighbors:
        s = neighbors[neighbor]
        y[neighbor] = numpy.zeros(datapoints, numpy.float64)
        for flow in s:
            ts = flow.date.timestamp() / (60 * 60 * 24)
            weights = normalization_factor * numpy.exp( - (x_date_in_days - ts) ** 2 / (2 * square_sigma) )
            y[neighbor] = y[neighbor] + (weights * flow.volume) * sign
            

    stackgroup = "suppliers"
    if flow_direction == "out":
        stackgroup = "consumers"
    for neighbor in y:
        fig.add_trace(Scatter(
            x=x_dates, y=y[neighbor],
            mode='lines', 
            name=neighbor, 
            line=dict(width=0.5, color=colorhash.ColorHash(neighbor).hex),
            stackgroup=stackgroup
        ))

plotly.io.renderers.default = "firefox"
    
fig.update_layout(
    title="LNG Supplier for " + options.zone + " / " + options.installation, 
    yaxis_title="inflow [cubic meters / day]"
)
fig.show()

db_cursor.close()
