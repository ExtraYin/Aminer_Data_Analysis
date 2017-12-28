#!/bin/bash

echo "Exporting Paper Info......"
sqlite3 -header -csv ./data/aminer.db "SELECT paper_id AS 'paperId:ID', paper_title AS 'title', year FROM DBLP_V10;" > ./data/papers.csv
echo "Exporting Author Info......"
sqlite3 -header -csv ./data/aminer.db "SELECT DISTINCT author_name AS 'name:ID' FROM DBLP_V10_AUTHOR;" > ./data/authors.csv

echo "Exporting Relationship: WRITES......"
sqlite3 -header -csv ./data/aminer.db "SELECT author_name AS ':START_ID', paper_id AS ':END_ID' FROM DBLP_V10_AUTHOR;" > ./data/writes.csv
echo "Exporting Relationship: CITES......"
sqlite3 -header -csv ./data/aminer.db "SELECT paper_id AS ':START_ID', reference_id AS ':END_ID' FROM DBLP_V10_CITATION;" > ./data/citations.csv


neo4j-import --into ./data/graph.db --id-type string \
		 	 --nodes:PAPER ./data/papers.csv \
		 	 --nodes:AUTHOR ./data/authors.csv \
		 	 --relationships:WRITES ./data/writes.csv \
			 --relationships:CITES ./data/citations.csv \
			 --legacy-style-quoting false


rm ./data/papers.csv
rm ./data/authors.csv
rm ./data/writes.csv
rm ./data/citations.csv

# CREATE CONSTRAINT ON (paper:PAPER) ASSERT paper.id IS UNIQUE;
# CREATE CONSTRAINT ON (author:AUTHOR) ASSERT author.name IS UNIQUE;
# CREATE CONSTRAINT ON (venue:Venue) ASSERT venue.name IS UNIQUE;