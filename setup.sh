sqlite3 db.db < ./queries/load-trades.sql
sqlite3 db.db < ./queries/recreate-tidy-trades.sql

python ./tidy-trade-data.py
