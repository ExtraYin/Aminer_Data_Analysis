
create table ACM ( 
  paper_index INTEGER PRIMARY KEY NOT NULL,   -- index id of this paper
  paper_title TEXT NOT NULL,  -- paperTitle
  year DATE,               -- Year
  publication_venue TEXT,  -- publication venue
  abstract TEXT            -- Abstract
);

create table ACM_AUTHOR  (
  paper_index INTEGER NOT NULL, 
  author_name TEXT, 
  FOREIGN KEY(paper_index) REFERENCES acm(paper_index)
);  

create table ACM_CITATION (
  paper_index INTEGER NOT NULL, 
  reference_id TEXT NOT NULL,   -- the id of references of this paper
  FOREIGN KEY(paper_index) REFERENCES acm(paper_index), 
  FOREIGN KEY(reference_id) REFERENCES acm(paper_index)
);

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
