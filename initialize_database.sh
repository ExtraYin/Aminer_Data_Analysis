rm aminer.db

echo "Creating Schema."
sqlite3 aminer.db < create_schema.sql

echo "Start Inserting Data......"
python import_data.py

echo "Creating Index."
sqlite3 aminer.db < create_index.sql