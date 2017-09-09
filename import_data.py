import sqlite3
import tqdm

class PaperScanner(object):
    def __init__(self, cur):
        self.cur = cur
        self.prefix_dict = {
            '#!': 'abstract',
            '#%': 'reference_id',
            '#*': 'paper_title',
            '#@': 'authors',
            '#c': 'publication_venue',
            '#index': 'paper_index',
            '#t': 'year'
        }
        self.reset_content()
        
    def reset_content(self):
        self.content = {x: "null" for x in self.prefix_dict.values()}
        self.authors = []
        self.references = []
        
    def scan(self, text):
        if line == "\n":
            self.flush()
            return 0
        for prefix, name in self.prefix_dict.items():
            if text.startswith(prefix):
                content = text[len(prefix):].strip()
                self.content[name] = content
                if prefix == "#%":
                    self.references.append(content)
                elif prefix == "#@":
                    self.authors = [x.strip() for x in content.split(",")]
        return 1
    
    def flush(self):
        # Insert into ACM
        insert = "INSERT OR REPLACE INTO ACM VALUES(?, ?, ?, ?, ?)"
        what = (
            self.content["paper_index"], 
            self.content["paper_title"], 
            self.content["year"], 
            self.content["publication_venue"], 
            self.content["abstract"]
        )
        self.cur.execute(insert, what)
        
        # Insert into ACM Author
        for author in self.authors:
            insert = "INSERT INTO ACM_AUTHOR VALUES(?, ?)"
            what = (
                self.content["paper_index"], 
                author
            )
            self.cur.execute(insert, what)
            
        # Insert into Citation
        for ref in self.references:
            insert = "INSERT INTO ACM_CITATION VALUES(?, ?)"
            what = (
                self.content["paper_index"], 
                ref
            )
            self.cur.execute(insert, what)
        
        self.reset_content()
        
class AuthorScanner(object):
    def __init__(self, cur):
        self.cur = cur
        self.prefix_dict = {
            '#index': 'author_index',
            '#n': 'author_name',
            '#a': 'affiliations',
            '#pc': 'number_published',
            '#cn': 'number_citation',
            '#hi': 'h_index',
            '#pi': 'p_index', 
            '#upi': 'up_index', 
            '#t': 'keyterm'
        }
        self.reset_content()
        
    def reset_content(self):
        self.content = {x: "null" for x in self.prefix_dict.values()}
        
    def scan(self, text):
        if line == "\n":
            self.flush()
            return 0
        for prefix, name in self.prefix_dict.items():
            if text.startswith(prefix):
                content = text[len(prefix):].strip()
                self.content[name] = content
        return 1
    
    def flush(self):
        # Insert into AUTHOR
        insert = "INSERT OR REPLACE INTO AUTHOR VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)"
        what = (
            self.content["author_index"], 
            self.content["author_name"], 
            self.content["affiliations"], 
            self.content["number_published"], 
            self.content["number_citation"], 
            self.content["h_index"], 
            self.content["p_index"], 
            self.content["up_index"], 
            self.content["keyterm"]
        )
        self.cur.execute(insert, what)
        
        self.reset_content()
        
        
if __name__ == "__main__":        
    conn = sqlite3.connect('aminer.db')
    cur = conn.cursor()

    print("Importing AMiner-Author.txt")
    total_line = sum(1 for line in open("data/AMiner-Author.txt"))
    author_scanner = AuthorScanner(cur)
    with open("data/AMiner-Author.txt", "r") as f:
        with tqdm.tqdm(total=total_line) as pbar:
            for line in f:
                author_scanner.scan(line)
                pbar.update(1)
    conn.commit()
    cur.execute("SELECT COUNT(*) FROM AUTHOR;")
    print(cur.fetchone()[0], "rows inserted into AUTHOR.")

    print("Importing acm.txt")
    total_line = sum(1 for line in open("data/acm.txt"))
    paper_scanner = PaperScanner(cur)
    with open("data/acm.txt", "r") as f:
        with tqdm.tqdm(total=total_line) as pbar:
            for line in f:
                paper_scanner.scan(line)
                pbar.update(1)
    conn.commit()

    cur.execute("SELECT COUNT(*) FROM ACM;")
    print(cur.fetchone()[0], "rows inserted into ACM.")
    cur.execute("SELECT COUNT(*) FROM ACM_AUTHOR;")
    print(cur.fetchone()[0], "rows inserted into ACM_AUTHOR.")
    cur.execute("SELECT COUNT(*) FROM ACM_CITATION;")
    print(cur.fetchone()[0], "rows inserted into ACM_CITATION.")

    

    conn.close()