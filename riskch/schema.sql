-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS marketpool;
DROP TABLE IF EXISTS hist;

CREATE TABLE marketpool (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  issue TEXT UNIQUE NOT NULL,
  fromdate TIMESTAMP NOT NULL,
  todate TIMESTAMP NOT NULL,
  car25 INTEGER NOT NULL
);

CREATE TABLE hist (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  issue_id TEXT NOT NULL,
  trade_id INTEGER NOT NULL,
  retrun_d REAL NOT NULL,
  FOREIGN KEY (issue_id) REFERENCES marketpool (id)
);
