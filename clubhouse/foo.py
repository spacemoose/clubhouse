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
# Right now I haven't gotten very far past fixing the couple of bugs
# in the original repo.

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

from clubhouse_resources import Story

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

# Problem 1: We have a bunch of stories imported from github.  They
# have an "external id", which looks like:
#    - https://api.github.com/repos/YUNEEC/Firmware/issues/2986
# ditch the "api." and the "/repos", and this is the correct link to the github issue.
#
# this should be a nice and easy fix:
#
# 1. find all stories with a non null "external id".
# 2. look for "api.github.com/repos/" and turn it into "github.com/"
# 3. save the modified external id.
def search_stories( query):

#    payload = {'page_size':100, 'query':query}
    ss_url = clubhouse_api_url+"/api/v2/search/stories"
    r = requests.get(ss_url, params = {'query':query, 'token':clubhouse_token})
#    print (r.url)
    r.encoding='utf-8'
    nxt = r.json()['next']
    retval = r.json()['data']
    while nxt is not None:
        nxt = nxt[nxt.rfind("=")+1:]
        print (nxt)
        r = requests.get(ss_url,
                         params = {'query':query, 'next':nxt,'token':clubhouse_token, })
###        print(r.url)
        print (r.status_code)

        nxt = r.json()['next']
        data = r.json()['data']
        retval += data
    print (len(retval))

def split_nxt(nxt):
    print(nxt)
    pos = nxt.find("query")
    return nxt[:pos], nxt[pos:]

def fix_github_links():
    stories = search_stories()
    modified=[]

    for story in r.json()['data']:
        if story['external_id'] is not None :
            if "api" in story['external_id']:
                story['external_id'] = story['external_id'].replace("api.github.com/repos", "github.com")
                modified.append(story)
    for story in modified :
        print(story['id'],story['external_id'])


def main():
#    update_clubhouse_resources()
    stories=search_stories("has:comment")

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
