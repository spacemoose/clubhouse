# Goal 1 is to import open issues from github, without importing
# duplicates, and subject to certain filters.
#
# I have no idea what I'm doing, so I'm going step by step trying
# stuff out.  Some of that might be useful to someone, so I'm storing
# it here.
#
# I started with this https://github.com/mahmoudimus/clubhouse, which
# seemed to be a nice start, but seems abandoned now.  This is my
# attempt to build something usable starting with that.
#
# Right now I haven't gotten very far past fixing the couple of bugs
# in the original repo.


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
    f = open("clubouse_resources.py", 'w')
    f.write(rendered)


def main():
    update_clubhouse_resources()


if __name__ == '__main__':
    main()
