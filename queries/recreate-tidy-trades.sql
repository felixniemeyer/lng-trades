DROP TABLE IF EXISTS tidy_trades; 

CREATE TABLE tidy_trades (
    id INTEGER PRIMARY KEY,
    origin TEXT, 
    destination TEXT, 
    orig_volume INTEGER, 
    dest_volume INTEGER, 
    orig_date INTEGER, 
    dest_date INTEGER
);
