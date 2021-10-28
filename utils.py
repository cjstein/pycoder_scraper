from pathlib import Path
from bs4 import BeautifulSoup
import feedparser
import sqlite3
import requests


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
        body text NOT NULL
        );
        """)
        return None

    def to_article(self, issue, title, url, body):
        return Article(issue, title, url, body)

    def insert_article(self, issue, title, url, body):
        self.cursor.execute(f"""
        INSERT INTO articles (issue, title, url, body) VALUES (?, ?, ?, ?)
        """, (issue, title, url, body))
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

    def search_articles(self, search_term):
        self.cursor.execute(f"""
        SELECT * FROM articles WHERE body LIKE ?
        """, (f'%{search_term}%',))
        # return self.cursor.fetchall()
        articles = self.cursor.fetchall()
        # for article in articles:
        #     print(*article)
        return [self.to_article(*article[1:]) for article in articles]


class Article:
    """
    Article class for storing and retrieving articles from the database.
    """
    def __init__(self, issue, title, url, body):
        self.issue = issue
        self.title = title
        self.url = url
        self.body = body

    def __str__(self):
        return f"{self.issue} - {self.title}"

    def __repr__(self):
        return f"{self.issue} - {self.title}"

    def to_db(self):
        return self.issue, self.title, self.url, self.body

    @property
    def issue_url(self):
        return f"https://pycoders.com/issues/{self.issue}"

