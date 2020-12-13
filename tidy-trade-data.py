import sqlite3

# local
import Utils

column_names = ["Vessel", "Zone Origin", "Installation origin", "End (origin)", "Zone Destination", "Installation Destination", "Start (destination)", "Volume (origin m3)", "Zone Canal Transit", "Volume (destination m3)", "Vessel type", "Trade status", "Ton Miles", "Subcontinent (origin)", "Subcontinent (destination)", "Start (origin)", "Seller (origin)", "Reload STS Partial (origin)", "Reload STS Partial (destination)", "Power plant type (vessel)", "Origin PortCall Id", "Origin", "Link3 type", "Link3 seller name", "Link3 seller country", "Link3 delivery", "Link3 buyer name", "Link3 buyer country", "Link2 type", "Link2 seller name", "Link2 seller country", "Link2 delivery", "Link2 buyer name", "Link2 buyer country", "Link1 type", "Link1 seller name", "Link1 seller country", "Link1 delivery", "Link1 buyer name", "Link1 buyer country", "Intermediaries", "IMO (vessel)", "Eta source (destination)", "Eta (origin)", "Eta (destination)", "End (destination)", "Destination PortCall Id", "Destination", "Delivery date (vessel)", "Date Start STS 2", "Date Start STS 1", "Date End STS 2", "Date End STS 1", "Date (origin)", "Date (destination)", "Country STS 2", "Country STS 1", "Country (origin)", "Country (destination)", "Continent Origin", "Continent Destination", "Charterer", "Cargo type (vessel)", "Cargo system (vessel)", "Cargo (tons)", "Cargo (origin tons)", "Cargo (destination tons)", "Capacity (vessel)", "Capacity (vessel m3)", "Buyer (destination)"]
column_dict = {}
i = 0
for column_name in column_names:
    column_dict[column_name] = i
    i += 1

db_connection = sqlite3.connect('db.db')
select_cur = db_connection.cursor()
insert_cur = db_connection.cursor()

node_names = []
node_inflows = []
node_outflows = []
insert_cur.execute('BEGIN TRANSACTION')
batchsize = 0
for row in select_cur.execute("SELECT * from trades"):
    origin = row[column_dict["Zone Origin"]] + " / " + row[column_dict["Installation origin"]]
    destination = row[column_dict["Zone Destination"]] + " / " + row[column_dict["Installation Destination"]]
    if destination == " - ": 
        continue
    orig_volume = row[column_dict["Volume (origin m3)"]]
    dest_volume = row[column_dict["Volume (destination m3)"]]
    try: 
        orig_date = Utils.parse_datetime(row[column_dict["Date (origin)"]]).timestamp()
    except Exception as e: 
        print("no orig date")
        orig_date = None
    try: 
        dest_date = Utils.parse_datetime(row[column_dict["Date (destination)"]]).timestamp()
    except Exception as e: 
        print("no dest date")
        dest_date = None    
    delivered = row[column_dict["Trade status"]] == "Delivered"
    value_names = [
        "origin", 
        "destination", 
        "orig_volume", 
        "dest_volume", 
        "orig_date", 
        "dest_date", 
        "delivered"
    ]
    query = 'INSERT OR IGNORE INTO tidy_trades ({}) VALUES ({})'.format(",".join(value_names), ",".join(["?"]*len(value_names)))
    values = (origin, destination, orig_volume, dest_volume, orig_date, dest_date, delivered)
    insert_cur.execute(query, values)
    batchsize += 1
    if(batchsize > 10000):
        insert_cur.execute('COMMIT')
        insert_cur.execute('BEGIN TRANSACTION')
insert_cur.execute('COMMIT')

select_cur.close()
insert_cur.close()
