import re
from typing import NamedTuple, Optional, List
from bs4 import BeautifulSoup
import requests

ISSUES_URL = "https://pycoders.com/issues"
HTML_PARSER = "html.parser"
SPONSOR = "sponsor"


class Article(NamedTuple):
    name: str
    url: str
    description: str
    issue: int
    source: Optional[str]


def create_soup_obj_from_url(url):
    resp = requests.get(url)
    return BeautifulSoup(resp.text, HTML_PARSER)


def get_articles_sections(soup, target_tag, substr_title):
    """
    Takes html between two tags, e.g. h2, the first one
    containing substr_title, e.g. "Articles"
    """
    html = ""
    for tag in soup.findAll(target_tag):
        if substr_title in tag.text:
            for tag in tag.next_siblings:
                if tag.name == target_tag:
                    break
                else:
                    html += str(tag)
    return html


def get_issue_link_ids(soup) -> List[int]:
    """
    Get all the issue ids
    """
    ids = [
        int(re.sub(r"^.*?(\d+)$", r"\1", a["href"]))
        for a in soup.findAll("a")
        if re.match(r"^/issues/\d+$", a["href"])
    ]
    return ids


def get_articles_from_issue(soup, skip_sponsor_links=True, issue_id=None):
    """
    Extract all articles from issue html
    """
    urls_done = set()
    for link in soup.findAll("a"):
        # avoid duplicated links
        if link["href"] in urls_done:
            continue

        urls_done.add(link["href"])

        # only look at main links, not the ones in the description
        if "color: #3399CC" not in str(link):
            continue

        description = link.findNext("span")

        if "font-family:georgia" not in str(description):
            continue
        source = description.findNext("span")
        tag = source and source.findNext("span")

        if tag and skip_sponsor_links and SPONSOR in str(tag):
            continue

        source = source.text if source else None
        yield Article(
            name=link.text,
            url=link["href"],
            description=description.text,
            source=source,
            issue=issue_id,
        )


if __name__ == "__main__":
    soup = create_soup_obj_from_url(ISSUES_URL)

    ids = get_issue_link_ids(soup)[:2]
    for id_ in ids:
        print(f"Issue {id_}")
        soup = create_soup_obj_from_url(f"{ISSUES_URL}/{id_}")
        html = get_articles_sections(soup, "h2", "Article")
        soup = BeautifulSoup(html, HTML_PARSER)
        for article in get_articles_from_issue(soup, issue_id=id_):
            print(article)
        print()
