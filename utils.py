from pathlib import Path
from bs4 import BeautifulSoup
import feedparser
import requests


def get_or_create_db() -> Path:
    """
    Gets or creates the database
    :return: full_path to the database
    """
    db_path = Path(__file__).parent / "db.sqlite3"
    if not db_path.exists():
        print("Creating database")
    else:
        print("Database already exists")
    return db_path


def parse_issue_contents(feed_entry: feedparser.util.FeedParserDict):
    """
    Parses the issue page
    :param feed_entry: it is a dictionary with the contents of the issue using the feedparser library
    :return:
    """
    pass
