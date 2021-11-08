"""
This file is the high level flow of the program.  Most the action can be found in the util.py file.
"""
import argparse
import utils
import scrapper


def main():
    print("main loop")
    db = utils.Database()
    db.create_table()
    latest_issue = db.get_latest_issue_number()
    soup = scrapper.create_soup_obj_from_url(scrapper.ISSUES_URL)

    ids = scrapper.get_issue_link_ids(soup)
    for id_ in ids:
        if id_ <= latest_issue:
            continue
        print(f"Issue {id_}")
        soup = scrapper.create_soup_obj_from_url(f"{scrapper.ISSUES_URL}/{id_}")
        html = scrapper.get_articles_sections(soup, "h2", "Article")
        soup = scrapper.BeautifulSoup(html, scrapper.HTML_PARSER)
        for article in scrapper.get_articles_from_issue(soup, issue_id=id_):
            print(article)
            article_page = utils.Article(article.name, article.url, article.issue, article.description, article.source)
            title, url, issue, description, source = article_page.to_db()
            db.insert_article(title, url, issue, description, source)
        print()


def search_db(search_term: str):
    db = utils.Database()
    articles = db.search_articles(search_term)
    for article in articles:
        print(article)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A tool for downloading and searching Pycoder\'s emails and articles')
    parser.add_argument('--search', '-s', nargs=1, help='Enter a search term to find related articles')
    search = parser.parse_args().search
    if search:
        search_db(search[0])
    else:
        main()
