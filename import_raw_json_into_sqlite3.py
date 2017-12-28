import os
import json
import tqdm
import sqlite3

def add_paper_info(cur, paper_id, paper_title, year, venue, abstract):
    insert = "INSERT OR REPLACE INTO DBLP_V10 VALUES(?, ?, ?, ?, ?)"
    what = (
        paper_id, 
        paper_title, 
        year, 
        venue, 
        abstract
    )
    cur.execute(insert, what)
    
def add_paper_author(cur, paper_id, author_name):
    insert = "INSERT INTO DBLP_V10_AUTHOR VALUES(?, ?)"
    what = (
        paper_id, 
        author_name
    )
    cur.execute(insert, what)
    
def add_paper_reference(cur, paper_id, reference_id):
    insert = "INSERT INTO DBLP_V10_CITATION VALUES(?, ?)"
    what = (
        paper_id, 
        reference_id
    )
    cur.execute(insert, what)

def add_paper(cur, paper):
    paper_id = paper["id"]
    paper_title = paper["title"]
    paper_year = paper.get("year", "NULL")
    venue = paper.get("venue", "NULL")
    abstract = paper.get("abstract", "NULL")
    add_paper_info(cur, paper_id, paper_title, paper_year, venue, abstract)
    
    for ref_id in paper.get("references", []):
        if ref_id:
            add_paper_reference(cur, paper_id, ref_id)
        
    for author_name in paper.get("authors", []):
        if author_name:
            add_paper_author(cur, paper_id, author_name)
            
if __name__ == "__main__":
    dblp_v10_json_files = [
        './data/raw/dblp-ref/dblp-ref-0.json', 
        './data/raw/dblp-ref/dblp-ref-1.json', 
        './data/raw/dblp-ref/dblp-ref-2.json', 
        './data/raw/dblp-ref/dblp-ref-3.json'
    ]

    sqlite_database_path = './data/aminer.db'
    conn = sqlite3.connect(sqlite_database_path)
    cur = conn.cursor()

    for dblp_v10_file in dblp_v10_json_files:
        print("Importing {} data into sqlite3 database......".format(dblp_v10_file))
        total_line = sum(1 for line in open(dblp_v10_file))

        with open(dblp_v10_file, 'r') as f, tqdm.tqdm(total=total_line) as pbar:
            for line in f:
                paper = json.loads(line)
                add_paper(cur, paper)
                pbar.update(1)

        conn.commit()

    cur.execute("SELECT COUNT(*) FROM DBLP_V10;")
    print(cur.fetchone()[0], "rows inserted into DBLP_V10.")
    cur.execute("SELECT COUNT(*) FROM DBLP_V10_AUTHOR;")
    print(cur.fetchone()[0], "rows inserted into DBLP_V10_AUTHOR.")
    cur.execute("SELECT COUNT(*) FROM DBLP_V10_CITATION;")
    print(cur.fetchone()[0], "rows inserted into DBLP_V10_CITATION.")