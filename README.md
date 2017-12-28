# Aminer_Data_Analysis

### Instructions

1. Install <a href="http://sqlite.org/">SQLite3</a> and <a href="https://neo4j.com/">Neo4j</a>

2. Download and import DBLP data into both SQLite3 and Neo4j.
```
./download_raw_data.sh
./import_raw_json_into_sqlite3.sh
./import_data_from_sqlite3_to_neo4j.sh
```

Move ./data/graph.db folder to YOUR_PATH_TO_NEO4J/data/databases and start Neo4j database by: `neo4j console`