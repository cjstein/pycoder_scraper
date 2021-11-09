from pathlib import Path
import sqlite3


class Database:
    """
    Database class for storing and retrieving articles from the database.
    """
    def __init__(self):
        self.db_path = Path(__file__).parent / "db.sqlite3"
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.latest_issue = 0

    def create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles(
        id integer PRIMARY KEY,
        issue integer NOT NULL,
        title text NOT NULL,
        url text NOT NULL,
        body text NOT NULL,
        source_info text
        );
        """)
        return None

    def to_article(self, title, url, issue, description, source):
        return Article(title, url, issue, description, source)

    def insert_article(self, title, url, issue, description, source):
        self.cursor.execute(f"""
        INSERT INTO articles (issue, title, url, body, source_info) VALUES (?, ?, ?, ?, ?)
        """, (issue, title, url, description, source))
        self.conn.commit()

    def get_articles(self):
        self.cursor.execute("""SELECT * FROM articles""")
        articles = self.cursor.fetchall()
        return [self.to_article(*article) for article in articles]

    def close(self):
        self.conn.close()

    def get_latest_issue_number(self):
        self.cursor.execute("""SELECT MAX(issue) FROM articles""")
        self.latest_issue = self.cursor.fetchone()[0]
        return self.latest_issue if self.latest_issue else 0

    def get_issues_from_db(self):
        self.cursor.execute("""SELECT DISTINCT issue FROM articles""")
        issues = self.cursor.fetchall()
        return [issue[0] for issue in issues]

    def search_articles(self, search_term):
        self.cursor.execute(f"""
        SELECT * FROM articles WHERE body LIKE ?
        """, (f'%{search_term}%',))
        articles = self.cursor.fetchall()
        return [self.to_article(*article[1:]) for article in articles]


class Article:
    """
    Article class for storing and retrieving articles from the database.
    """
    def __init__(self, title, url, issue, description, source):
        self.issue = issue
        self.title = title
        self.url = url
        self.description = description
        self.source = source

    def __str__(self):
        return f"{self.issue} || {self.title} || {self.description} || {self.url}"

    def __repr__(self):
        return f"Article({self.issue}, {self.title}"

    def to_db(self):
        return self.title, self.url, self.issue, self.description, self.source

    @property
    def issue_url(self):
        return f"https://pycoders.com/issues/{self.issue}"

