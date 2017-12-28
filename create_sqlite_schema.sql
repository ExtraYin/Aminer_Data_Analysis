
create table DBLP_V10 ( 
  paper_id TEXT PRIMARY KEY NOT NULL,   -- index id of this paper
  paper_title TEXT,   -- paperTitle
  year DATE,      -- Year
  venue TEXT,     -- publication venue
  abstract TEXT   -- Abstract
);

create table DBLP_V10_AUTHOR (
  paper_id TEXT NOT NULL, 
  author_name TEXT, 
  FOREIGN KEY(paper_id) REFERENCES DBLP_V10(paper_id)
);  

create table DBLP_V10_CITATION (
  paper_id TEXT NOT NULL, 
  reference_id TEXT NOT NULL,   -- the id of references of this paper
  FOREIGN KEY(paper_id) REFERENCES DBLP_V10(paper_id)
);

/*
create table AUTHOR (
  author_index INTEGER PRIMARY KEY NOT NULL,      -- index id of this author
  author_name TEXT NOT NULL,   -- name  (separated by semicolons)
  affiliations TEXT,           -- affiliations  (separated by semicolons)
  number_published INTEGER CHECK(number_published>=0),    -- the number of published papers of this author
  number_citation INTEGER CHECK(number_citation>=0),      -- the total number of citations of this author
  h_index REAL CHECK(h_index>=0),                      -- the H-index of this author
  p_index REAL CHECK(p_index>=0),                      -- the P-index with equal A-index of this author
  up_index REAL CHECK(up_index>=0),                    -- the P-index with unequal A-index of this author
  keyterm TEXT    -- extracted keyterms of this author  (separated by semicolons)
);
*/
