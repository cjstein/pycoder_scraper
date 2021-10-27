"""
This file is the high level flow of the program.  Most the action can be found in the util.py file.
"""
import argparse
import utils


def main():

    # TODO Check to see if a DB has been created, if so, load it and update it, else create a new one and populate it.
    # TODO Load the feed
    # TODO determine which issues are new and which ones have been already entered
    # TODO cycle through the Entries of new ones
    # TODO parse the entry, load it into the database
    print("main loop")
    print(utils.get_or_create_db())


def search_db(search_term: str):
    print(f'Search loop for {search_term}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A tool for downloading and searching Pycoder\'s emails and articles')
    parser.add_argument('--search', '-s', nargs=1, help='Enter a search term to find related articles')
    search = parser.parse_args().search
    if search:
        search_db(search[0])
    else:
        main()
