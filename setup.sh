sqlite3 db.db < ./queries/load-trades.sql
sqlite3 db.db < ./queries/recreate-tidy-trades.sql

echo "creating directories if they don't exist yet"
mkdir results
mkdir plots

python ./tidy-trade-data.py

for create_view_query in ./queries/views/*.sql; do
    echo "creating view $create_view_query"
    sqlite3 db.db < $create_view_query
done
