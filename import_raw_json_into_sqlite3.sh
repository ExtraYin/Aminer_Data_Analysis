#!/bin/bash

echo "Creating SQLite schema......"
sqlite3 ./data/aminer.db < create_sqlite_schema.sql

echo "Importing data into SQLite database......"
Python import_raw_json_into_sqlite3.py

echo "Cleaning......"
rm -rf ./data/raw/dblp-ref