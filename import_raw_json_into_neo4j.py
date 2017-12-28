import os
import tqdm
import json
from neo4j.v1 import GraphDatabase, basic_auth

def create_schema(session):
    # Create uniqueness constraint
    session.run("CREATE CONSTRAINT ON (paper:Paper) ASSERT paper.id IS UNIQUE")
    session.run("CREATE CONSTRAINT ON (author:Author) ASSERT author.name IS UNIQUE")
    session.run("CREATE CONSTRAINT ON (venue:Venue) ASSERT venue.name IS UNIQUE")
    
def add_reference(session, paper_id, paper_title, reference_paper_id):
    session.run("MERGE (p1:Paper {id: {paper_id}}) "
                "SET p1.title = {paper_title}"
                "MERGE (p2:Paper {id: {reference_paper_id}}) "
                "MERGE (p1)-[:CITES]->(p2)", 
                paper_id = paper_id, paper_title=paper_title, 
                reference_paper_id = reference_paper_id)
    
def add_author(session, paper_id, paper_title, author_name):
    session.run("MERGE (a:Author {name: {author_name}}) "
                "MERGE (p:Paper {id: {paper_id}}) "
                "SET p.title = {paper_title}"
                "MERGE (a)-[:WRITES]->(p)", 
                paper_id = paper_id, paper_title=paper_title, 
                author_name = author_name)
    
def add_venue(session, paper_id, paper_title, venue_name):
    session.run("MERGE (v:Venue {name: {venue_name}}) "
                "MERGE (p:Paper {id: {paper_id}}) "
                "SET p.title = {paper_title}"
                "MERGE (v)-[:PUBLISHES]->(p)", 
                paper_id = paper_id, paper_title = paper_title, 
                venue_name = venue_name)
    
def add_paper(session, paper):
    paper_id = paper["id"]
    paper_title = paper["title"]
    for ref_id in paper.get("references", []):
        if ref_id:
            add_reference(session, paper_id, paper_title, ref_id)
        
    for author_name in paper.get("authors", []):
        if author_name:
            add_author(session, paper_id, paper_title, author_name)
    
    if "venue" in paper and paper['venue']:
        add_venue(session, paper_id, paper_title, paper['venue'])
        
if __name__ == "__main__":
    dblp_v10_json_files = [
        './data/raw/dblp-ref/dblp-ref-0.json', 
        './data/raw/dblp-ref/dblp-ref-1.json', 
        './data/raw/dblp-ref/dblp-ref-2.json', 
        './data/raw/dblp-ref/dblp-ref-3.json'
    ]
    
    uri = "bolt://localhost:7687"
    auth_token = basic_auth("neo4j", "password")
    driver = GraphDatabase.driver(uri, auth=auth_token, encrypted=False)
    
    with driver.session() as session:
        print("Creating uniqueness constraints......")
        create_schema(session)
    
        for dblp_v10_file in dblp_v10_json_files:
            print("Importing {} data into neo4j database......".format(dblp_v10_file))
            total_line = sum(1 for line in open(dblp_v10_file))

            with open(dblp_v10_file, 'r') as f, tqdm.tqdm(total=total_line) as pbar:
                for line in f:
                    paper = json.loads(line)
                    add_paper(session, paper)
                    pbar.update(1)