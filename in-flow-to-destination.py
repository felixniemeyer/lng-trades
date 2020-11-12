import sqlite3
import datetime
import Utils
import math
import numpy
import scipy
import plotly
import colorhash

db_connection = sqlite3.connect('db.db')
db_cursor = db_connection.cursor()

zone = "Huelva"
installation = "Huelva"

query = open("./query-templates/in-flows-of-a-node.sql").read()
query = query.replace('$zone', zone)
query = query.replace('$installation', installation)

class Flow:
    def __init__(self, volume, date):
        self.volume = volume
        self.date = date
    def __repr__(self):
        return self.volume.__str__() + ", " + self.date.__str__()

suppliers = {}
init_date_range = True
for row in db_cursor.execute(query):
    try: 
        supplier = row[0] + ' / ' + row[1]
        volume = int(row[2])
        date = Utils.parse_datetime(row[3])
        if not supplier in suppliers:
            suppliers[supplier] = []
        suppliers[supplier].append(Flow(volume, date))
        
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
        print("couldn't handle the row", row, "because", e) 
            
kernel_width = 30 * 24 * 60 

# TODO! check that based on the kernel width, from_date and to_date are far enough apart
# move from_date and to_date each by kernel width closer together

from_date = datetime.datetime(2020, 2, 1)
to_date = datetime.datetime(2020, 6, 15)
stepsize = datetime.timedelta(days=2)
datapoints = math.ceil( (to_date - from_date) / stepsize ) 

x_dates = numpy.empty(datapoints, 'datetime64[D]')
x_secs = numpy.empty(datapoints, numpy.uint64)
for i in range(datapoints):
    dt = from_date + i * stepsize
    x_dates[i] = dt
    x_secs[i] = dt.timestamp() / 60

#30 days in minutes
sigma = Utils.fwhm2sigma(30 * 24 * 60) 
square_sigma = sigma ** 2 
normalization_factor = 1 / ( sigma * math.sqrt(2 * math.pi) )

y = {}
for supplier in suppliers:
    s = suppliers[supplier]
    y[supplier] = numpy.zeros(datapoints, numpy.float64)
    for flow in s:
        ts = flow.date.timestamp() / 60
        weights = normalization_factor * numpy.exp( - (x_secs - ts) ** 2 / (2 * square_sigma) )
        y[supplier] = y[supplier] + (weights * flow.volume)
        

plotly.io.renderers.default = "firefox"

Scatter = plotly.graph_objects.Scatter
fig = plotly.graph_objects.Figure()
for supplier in y:
    fig.add_trace(Scatter(
        x=x_dates, y=y[supplier],
        mode='lines', 
        name=supplier, 
        line=dict(width=0.5, color=colorhash.ColorHash(supplier).hex),
        stackgroup='suppliers'
    ))

fig.update_layout(
    title="LNG Supplier for " + zone + " / " + installation, 
    yaxis_title="cubic meters / minute"
)
fig.show()

db_cursor.close()