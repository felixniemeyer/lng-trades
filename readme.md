## setup
```shell
./setup.sh
```
will import data from ```data/lng-trades.csv``` into a sqlite db stored in ```./db.db```.

## some requiremed python libraries
```shell
pip install colorhash
```

## sql queries
execute queries like this: 
``` shell
sqlite3 db.db < queries/query.sql

## for the jupyter lab 
install jupyter according to one way (explained here)[https://jupyterlab.readthedocs.io/en/stable/getting_started/installation.html]

install the plotly extension:
```bash
jupyter labextension install jupyterlab-plotly
```

## execute a query template
replace placeholders with sed
```bash
sqlite3 db.db "`cat query-templates/in-flows-of-a-node.sql | sed 's/$zone/Huelva/g; s/$installation/Huelva/g'`"
```
