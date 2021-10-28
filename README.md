# Pycoder Issue Scrapper
This is a simple script that scrapes the issues from pycoder's archive repo and outputs them to a database that is searchable.

### Installation
First clone the repo then install the requirements

    pip install -r requirements.txt

### Usage
##### Creating and updating the database
To create the DB the first time or update it run the following command:

    python main.py


##### Searching the database
To search the database run the following command with the -s or --search flag:

    python main.py -s <search term>

or

    python main.py --search <search term>

This will print out a list of the issues that match the search term,
along with the snippet of the article it came from in the issue for where it was found.
