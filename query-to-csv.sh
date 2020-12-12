query="`cat $1`"
sqlite3 db.db -cmd ".mode csv" ".headers on" ".output $2" ".schema" "`echo $query`"

