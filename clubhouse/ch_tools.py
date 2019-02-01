# Goal 1 is to import open import from github, without importing
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
# At the moment I'm just writing some super simple stuff working
# directly with dictionaries.

import requests
import importlib
import parser
from lxml import html
from io import StringIO
import os
import sys
import json
import curlify

from pprint import pprint

#from clubhouse_resources import Story

clubhouse_token=os.environ['CLUBHOUSE_TOKEN']
clubhouse_api_url = "https://api.clubhouse.io"


# Parse the Resources section from Clubhouse's documentation and
# generate marshmallow schemas that can be sued for interacting with
# the API.
def update_clubhouse_resources():
    r = requests.get("https://clubhouse.io/api/rest/v2/")
    f = open("specs.html", 'w')
    r.encoding='utf-8'
    f.write(r.text)
    parsed = parser.parse(html.parse("specs.html"))
    munged = parser.munge(parsed)
    rendered = parser.build(munged)
    f = open("clubhouse_resources.py", 'w')
    f.write(rendered)

# This returns list of stories (as a dictionary) that satisfy the
# passed query.  The query parameter is the same query string you use
# to searc in the clubhouse interface.
def search_stories( query):
    print ("gathering clubhouse stories", end='', flush=True)
    ss_url = clubhouse_api_url+"/api/v2/search/stories"
    r = requests.get(ss_url, params = {'query':query, 'token':clubhouse_token})
    r.encoding='utf-8'
    nxt = r.json()['next']
    retval = r.json()['data']
    while nxt is not None:
        nxt = nxt[nxt.rfind("=")+1:]
        r = requests.get(ss_url,
                         params = {'query':query, 'next':nxt,'token':clubhouse_token, })
        nxt = r.json()['next']
        data = r.json()['data']
        retval += data
        print(".", end='', flush=True)
    print(f"\ncollected {len(retval)} stories")
    return retval

def fix_github_links(stories):
    modified=[]
    for story in stories:
        if story['external_id'] is not None :
            if "api" in story['external_id']:
                story['external_id'] = story['external_id'].replace("api.github.com/repos", "github.com")
                modified.append(story)
                break
    print(f"found {len(modified)} stories with mangled external_id")

#   for story in modified :
#       print(story['id'],story['external_id'])

# Given a github issue number, import that issue from github!
#def import_issue(github_number):


def main():
    stories=search_stories("has:comment")
    fix_github_links(stories)
if __name__ == '__main__':
    main()


# Let's try reading something from clubhouse:
#  1. Get list of open stories in clubhouse.
#  2. Get list of recently (param date) closed stories in clubhouse.
#
#  a) gonna need an authentication token.
#  b) clubouse will barf ifmore than 200 requests per minute.


# TODOS
#   1. fix all the github api links.
#   2. correctly import github api stuff, without impoting duplicates.
#   3. sync states between github and clubhouse stories.

# I can't get authentication via token to work in requests, so pass
# the user and password by commnd line for now.
