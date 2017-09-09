CREATE INDEX idx_ACM_on_paper_title ON ACM(paper_title);
CREATE INDEX idx_ACM_on_publication_venue ON ACM(publication_venue);

-- An index should be created on the child key columns of each foreign key constraint
CREATE INDEX idx_ACM_AUTHOR_on_paper_index ON ACM_AUTHOR(paper_index);
CREATE INDEX idx_ACM_AUTHOR_on_author_name ON ACM_AUTHOR(author_name);

CREATE INDEX idx_ACM_CITATION_on_paper_index ON ACM_CITATION(paper_index);
CREATE INDEX idx_ACM_CITATION_on_reference_id ON ACM_CITATION(reference_id);

CREATE INDEX idx_AUTHOR_on_author_index ON AUTHOR(author_index);
CREATE INDEX idx_AUTHOR_on_author_name ON AUTHOR(author_name);

