# Goal 1 is to import open issues from github, without importing
# duplicates, and subject to certain filters.

# This gets the api information from
import requests
import importlib
import parser
from lxml import html
from io import StringIO

clubhouse_url = "https://clubhouse.io"


# Parse the Resources section from Clubhouse's documentation and
# generate marshmallow schemas that can be sued for interacting with
# the API.
def update_clubhouse_resources():
    r = requests.get(clubhouse_url + "/api/rest/v2/")
    f = open("specs.html", 'w')
    r.encoding='utf-8'
    f.write(r.text)
    parsed = parser.parse(html.parse("specs.html"))
    munged = parser.munge(parsed)
    rendered = parser.build(munged)
    f = open(clubouse_resources.py)
    f.write(rendered)


def main():
    update_clubhouse_resources()


if __name__ == '__main__':
    main()
