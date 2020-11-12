
## execute a query template
replace placeholders with sed
```bash
sqlite3 db.db "`cat query-templates/in-flows-of-a-node.sql | sed 's/$zone/Huelva/g; s/$installation/Huelva/g'`"
```