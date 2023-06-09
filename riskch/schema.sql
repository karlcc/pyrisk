-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS marketpool;
DROP TABLE IF EXISTS hist;
DROP TABLE IF EXISTS eq_safef;

CREATE TABLE marketpool (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  issue TEXT UNIQUE NOT NULL,
  fromdate DATE NOT NULL,
  todate DATE NOT NULL,
  car25 REAL NOT NULL
);

CREATE TABLE hist (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  issue_id INTEGER NOT NULL,
  trade_id INTEGER NOT NULL,
  retrun_d REAL NOT NULL,
  FOREIGN KEY (issue_id) REFERENCES marketpool (id)
);

CREATE TABLE eq_safef (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  issue_id INTEGER NOT NULL,
  curve TEXT NOT NULL,
  FOREIGN KEY (issue_id) REFERENCES marketpool (id)
);